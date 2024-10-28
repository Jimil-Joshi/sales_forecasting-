# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from prophet import Prophet
import requests

st.set_page_config(page_title="Sales Forecasting", layout="wide")

st.title("Sales Forecasting Dashboard")

# Sidebar
st.sidebar.header("Forecast Parameters")
forecast_days = st.sidebar.slider("Forecast Days", 1, 365, 30)


# Load and display data
@st.cache_data
def load_data():
    df = pd.read_csv('data/train.csv')
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    return df


try:
    df = load_data()

    if st.button("Generate Forecast"):
        # Prepare data
        daily_sales = df.groupby('Order_Date')['Sales'].sum().reset_index()
        prophet_df = daily_sales.rename(columns={
            'Order_Date': 'ds',
            'Sales': 'y'
        })

        # Create and fit model
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            changepoint_prior_scale=0.05,
            seasonality_prior_scale=10.0
        )

        with st.spinner("Generating forecast..."):
            model.fit(prophet_df)
            future_dates = model.make_future_dataframe(periods=forecast_days)
            forecast = model.predict(future_dates)

            # Create plot
            fig = go.Figure()

            # Historical data
            fig.add_trace(go.Scatter(
                x=prophet_df['ds'],
                y=prophet_df['y'],
                name='Historical Sales',
                line=dict(color='blue', width=1)
            ))

            # Forecast
            fig.add_trace(go.Scatter(
                x=forecast['ds'].tail(forecast_days),
                y=forecast['yhat'].tail(forecast_days),
                name='Forecast',
                line=dict(color='red', width=2)
            ))

            # Confidence intervals
            fig.add_trace(go.Scatter(
                x=forecast['ds'].tail(forecast_days),
                y=forecast['yhat_upper'].tail(forecast_days),
                fill=None,
                mode='lines',
                line=dict(color='rgba(255,0,0,0)'),
                showlegend=False
            ))

            fig.add_trace(go.Scatter(
                x=forecast['ds'].tail(forecast_days),
                y=forecast['yhat_lower'].tail(forecast_days),
                fill='tonexty',
                mode='lines',
                line=dict(color='rgba(255,0,0,0)'),
                name='Confidence Interval',
                fillcolor='rgba(255,0,0,0.2)'
            ))

            fig.update_layout(
                title="Sales Forecast",
                xaxis_title="Date",
                yaxis_title="Sales ($)",
                template='plotly_white'
            )

            st.plotly_chart(fig, use_container_width=True)

            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Sales", f"${prophet_df['y'].sum():,.2f}")
            with col2:
                st.metric("Average Daily Sales", f"${prophet_df['y'].mean():,.2f}")
            with col3:
                trend = ((prophet_df['y'].tail(30).mean() -
                          prophet_df['y'].tail(60).head(30).mean()) /
                         prophet_df['y'].tail(60).head(30).mean() * 100)
                st.metric("30-Day Trend", f"{trend:,.1f}%")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")