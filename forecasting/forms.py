from django import forms

class ForecastForm(forms.Form):
    store = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    dept = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    forecast_weeks = forms.IntegerField(
        min_value=1,
        max_value=52,
        initial=12,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )