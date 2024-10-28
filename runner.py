import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from prophet import Prophet

st.set_page_config(page_title="Sales Forecasting", layout="wide")

st.title("Sales Forecasting Dashboard")

# Sidebar
st.sidebar.header("Forecast Parameters")
forecast_days = st.sidebar.slider("Forecast Days", 1, 365, 30)
selected_store = st.sidebar.number_input("Store Number", min_value=1, value=1, step=1)
selected_dept = st.sidebar.number_input("Department Number", min_value=1, value=1, step=1)


# Load and display data
@st.cache_data
def load_data():
    df = pd.read_csv('data/train.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df


try:
    df = load_data()

    # Filter data for selected store and department
    filtered_df = df[
        (df['Store'] == selected_store) &
        (df['Dept'] == selected_dept)
        ]

    if filtered_df.empty:
        st.warning("No data found for the selected store and department combination.")
    else:
        st.write(f"Showing data for Store {selected_store}, Department {selected_dept}")

        if st.button("Generate Forecast"):
            # Prepare data for Prophet
            prophet_df = filtered_df[['Date', 'Weekly_Sales']].rename(
                columns={'Date': 'ds', 'Weekly_Sales': 'y'}
            )

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
                future_dates = model.make_future_dataframe(
                    periods=forecast_days,
                    freq='W'  # Weekly frequency since we have weekly sales
                )
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
                    title=f"Sales Forecast - Store {selected_store}, Dept {selected_dept}",
                    xaxis_title="Date",
                    yaxis_title="Weekly Sales ($)",
                    template='plotly_white'
                )

                st.plotly_chart(fig, use_container_width=True)

                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Historical Sales", f"${prophet_df['y'].sum():,.2f}")
                with col2:
                    st.metric("Average Weekly Sales", f"${prophet_df['y'].mean():,.2f}")
                with col3:
                    trend = ((prophet_df['y'].tail(4).mean() -
                              prophet_df['y'].tail(8).head(4).mean()) /
                             prophet_df['y'].tail(8).head(4).mean() * 100)
                    st.metric("4-Week Trend", f"{trend:,.1f}%")

                # Add forecast summary
                st.subheader("Forecast Summary")
                forecast_summary = pd.DataFrame({
                    'Date': forecast['ds'].tail(forecast_days),
                    'Predicted Sales': forecast['yhat'].tail(forecast_days),
                    'Lower Bound': forecast['yhat_lower'].tail(forecast_days),
                    'Upper Bound': forecast['yhat_upper'].tail(forecast_days)
                })
                st.dataframe(forecast_summary.round(2))

except Exception as e:
    st.error(f"An error occurred: {str(e)}")