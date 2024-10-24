from django import forms

class ForecastForm(forms.Form):
    forecast_days = forms.IntegerField(
        min_value=1,
        max_value=52,  # Maximum of 1 year (52 weeks)
        initial=12,    # Default to 12 weeks
        label='Forecast Weeks',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )