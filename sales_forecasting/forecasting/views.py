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
                # Get the number of days to forecast
                forecast_days = form.cleaned_data['forecast_days']

                # Load and prepare the data
                data_path = os.path.join(settings.BASE_DIR, 'data', 'train.csv')
                df = pd.read_csv(data_path)

                # Convert date and prepare daily sales data
                df['Order_Date'] = pd.to_datetime(df['Order_Date'])
                daily_sales = df.groupby('Order_Date')['Sales'].sum().reset_index()

                # Rename columns for Prophet
                prophet_df = daily_sales.rename(columns={
                    'Order_Date': 'ds',
                    'Sales': 'y'
                })

                # Sort by date
                prophet_df = prophet_df.sort_values('ds')

                # Create and fit the model with additional parameters
                model = Prophet(
                    yearly_seasonality=True,
                    weekly_seasonality=True,
                    daily_seasonality=False,
                    changepoint_prior_scale=0.05,
                    seasonality_prior_scale=10.0
                )

                model.fit(prophet_df)

                # Create future dates for forecasting
                future_dates = model.make_future_dataframe(periods=forecast_days)
                forecast = model.predict(future_dates)

                # Create the plot
                fig = go.Figure()

                # Add historical data
                fig.add_trace(go.Scatter(
                    x=prophet_df['ds'],
                    y=prophet_df['y'],
                    name='Historical Sales',
                    line=dict(color='blue', width=1),
                    mode='lines'
                ))

                # Add forecasted data
                fig.add_trace(go.Scatter(
                    x=forecast['ds'].tail(forecast_days),
                    y=forecast['yhat'].tail(forecast_days),
                    name='Forecast',
                    line=dict(color='red', width=2)
                ))

                # Add confidence intervals
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

                # Update layout with more detailed information
                fig.update_layout(
                    title={
                        'text': 'Superstore Sales Forecast',
                        'y': 0.95,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    xaxis_title='Date',
                    yaxis_title='Sales ($)',
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

                # Calculate some statistics for display
                total_sales = prophet_df['y'].sum()
                avg_daily_sales = prophet_df['y'].mean()
                last_30_days_trend = (
                                             prophet_df['y'].tail(30).mean() -
                                             prophet_df['y'].tail(60).head(30).mean()
                                     ) / prophet_df['y'].tail(60).head(30).mean() * 100

                context = {
                    'form': form,
                    'plot': plot_html,
                    'forecast_days': forecast_days,
                    'total_sales': f"${total_sales:,.2f}",
                    'avg_daily_sales': f"${avg_daily_sales:,.2f}",
                    'trend': f"{last_30_days_trend:,.1f}%"
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