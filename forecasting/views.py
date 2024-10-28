# forecasting/views.py
import pandas as pd
import plotly.graph_objects as go
from prophet import Prophet
from django.shortcuts import render
from .forms import ForecastForm
import os
from django.conf import settings


def index(request):
    return render(request, 'forecasting/index.html')


def forecast(request):
    if request.method == 'POST':
        form = ForecastForm(request.POST)
        if form.is_valid():
            try:
                # Get form data
                store = form.cleaned_data['store']
                dept = form.cleaned_data['dept']
                forecast_weeks = form.cleaned_data['forecast_weeks']

                # Load and prepare the data
                data_path = os.path.join(settings.BASE_DIR, 'data', 'train.csv')
                df = pd.read_csv(data_path)

                # Convert date and filter for specific store and department
                df['Date'] = pd.to_datetime(df['Date'])
                store_dept_data = df[(df['Store'] == store) & (df['Dept'] == dept)].copy()

                if store_dept_data.empty:
                    raise ValueError(f"No data found for Store {store} and Department {dept}")

                # Prepare data for Prophet
                prophet_df = store_dept_data[['Date', 'Weekly_Sales']].rename(
                    columns={'Date': 'ds', 'Weekly_Sales': 'y'}
                )

                # Add holiday flags
                holidays = store_dept_data[store_dept_data['IsHoliday']][['Date']].rename(
                    columns={'Date': 'ds'}
                )
                holidays['holiday'] = 'holiday'

                # Create and fit the model
                model = Prophet(
                    yearly_seasonality=True,
                    weekly_seasonality=True,
                    daily_seasonality=False,
                    changepoint_prior_scale=0.05,
                    seasonality_prior_scale=10.0,
                    holidays=holidays
                )

                model.fit(prophet_df)

                # Create future dates for forecasting
                future_dates = model.make_future_dataframe(periods=forecast_weeks, freq='W')
                forecast = model.predict(future_dates)

                # Create the plot
                fig = go.Figure()

                # Add historical data
                fig.add_trace(go.Scatter(
                    x=prophet_df['ds'],
                    y=prophet_df['y'],
                    name='Historical Sales',
                    line=dict(color='blue', width=1),
                    mode='lines+markers'
                ))

                # Add forecasted data
                fig.add_trace(go.Scatter(
                    x=forecast['ds'].tail(forecast_weeks),
                    y=forecast['yhat'].tail(forecast_weeks),
                    name='Forecast',
                    line=dict(color='red', width=2),
                    mode='lines+markers'
                ))

                # Add confidence intervals
                fig.add_trace(go.Scatter(
                    x=forecast['ds'].tail(forecast_weeks),
                    y=forecast['yhat_upper'].tail(forecast_weeks),
                    fill=None,
                    mode='lines',
                    line=dict(color='rgba(255,0,0,0)'),
                    showlegend=False
                ))

                fig.add_trace(go.Scatter(
                    x=forecast['ds'].tail(forecast_weeks),
                    y=forecast['yhat_lower'].tail(forecast_weeks),
                    fill='tonexty',
                    mode='lines',
                    line=dict(color='rgba(255,0,0,0)'),
                    name='Confidence Interval',
                    fillcolor='rgba(255,0,0,0.2)'
                ))

                # Add holiday markers
                holiday_dates = store_dept_data[store_dept_data['IsHoliday']]['Date']
                holiday_sales = store_dept_data[store_dept_data['IsHoliday']]['Weekly_Sales']

                fig.add_trace(go.Scatter(
                    x=holiday_dates,
                    y=holiday_sales,
                    mode='markers',
                    name='Holidays',
                    marker=dict(
                        size=10,
                        symbol='star',
                        color='yellow',
                        line=dict(color='black', width=1)
                    )
                ))

                # Update layout
                fig.update_layout(
                    title={
                        'text': f'Store {store} - Department {dept} Weekly Sales Forecast',
                        'y': 0.95,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    xaxis_title='Date',
                    yaxis_title='Weekly Sales ($)',
                    template='plotly_white',
                    hovermode='x unified',
                    legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01
                    ),
                    margin=dict(t=100, l=50, r=50, b=50)
                )

                # Add range slider
                fig.update_xaxes(rangeslider_visible=True)

                # Convert plot to HTML
                plot_html = fig.to_html(full_html=False, include_plotlyjs=True)

                # Calculate statistics
                total_sales = prophet_df['y'].sum()
                avg_weekly_sales = prophet_df['y'].mean()
                last_12_weeks_trend = (
                                              prophet_df['y'].tail(12).mean() -
                                              prophet_df['y'].tail(24).head(12).mean()
                                      ) / prophet_df['y'].tail(24).head(12).mean() * 100

                # Get number of holidays
                holiday_count = store_dept_data['IsHoliday'].sum()

                context = {
                    'form': form,
                    'plot': plot_html,
                    'store': store,
                    'dept': dept,
                    'forecast_weeks': forecast_weeks,
                    'total_sales': f"${total_sales:,.2f}",
                    'avg_weekly_sales': f"${avg_weekly_sales:,.2f}",
                    'trend': f"{last_12_weeks_trend:,.1f}%",
                    'holiday_count': holiday_count
                }

                return render(request, 'forecasting/forecast.html', context)

            except Exception as e:
                context = {
                    'form': form,
                    'error': f"An error occurred: {str(e)}"
                }
                return render(request, 'forecasting/forecast.html', context)
    else:
        form = ForecastForm()

    return render(request, 'forecasting/forecast.html', {'form': form})