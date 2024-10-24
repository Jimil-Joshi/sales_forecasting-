from django.urls import path
from . import views

app_name = 'forecasting'

urlpatterns = [
    path('', views.index, name='index'),
    path('forecast/', views.forecast, name='forecast'),
]