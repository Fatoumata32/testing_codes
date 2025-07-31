from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.weather_dashboard, name='dashboard'),
    path('api/current/', views.get_current_weather, name='current_api'),
]