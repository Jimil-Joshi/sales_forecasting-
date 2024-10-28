from django.db import models

class SalesData(models.Model):
    store = models.IntegerField()
    dept = models.IntegerField()
    date = models.DateField()
    weekly_sales = models.DecimalField(max_digits=12, decimal_places=2)
    is_holiday = models.BooleanField()

    class Meta:
        unique_together = ('store', 'dept', 'date')

class ForecastResult(models.Model):
    store = models.IntegerField()
    dept = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    forecast_weeks = models.IntegerField()
    total_sales = models.DecimalField(max_digits=12, decimal_places=2)
    avg_weekly_sales = models.DecimalField(max_digits=12, decimal_places=2)
    trend_percentage = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"Forecast for Store {self.store} Dept {self.dept} ({self.created_at})"
