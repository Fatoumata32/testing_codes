from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from .models import WeatherData
from django.utils import timezone
import requests

def get_current_weather(request):
    region = request.GET.get('region', 'dakar')
    
    try:
        # Essayer d'obtenir les données en cache
        weather = WeatherData.objects.filter(
            region__icontains=region,
            is_current=True
        ).first()
        
        if not weather:
            # Récupérer depuis l'API OpenWeatherMap si configurée
            api_key = settings.OPENWEATHER_API_KEY
            if api_key:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={region},SN&appid={api_key}&units=metric"
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    weather = WeatherData.objects.create(
                        region=region,
                        temperature=data['main']['temp'],
                        humidity=data['main']['humidity'],
                        wind_speed=data['wind']['speed'],
                        rain_chance=data.get('rain', {}).get('1h', 0) * 100,
                        visibility=data['visibility'] / 1000,
                        condition=data['weather'][0]['description'],
                        forecast_date=timezone.now().date(),
                        is_current=True
                    )
            else:
                # Données fictives si pas d'API
                import random
                weather_data = {
                    'temperature': f"{random.randint(25, 35)}°C",
                    'humidity': f"{random.randint(50, 80)}%",
                    'wind_speed': f"{random.randint(5, 20)} km/h",
                    'rain_chance': f"{random.randint(0, 60)}%",
                    'visibility': f"{random.randint(8, 15)} km",
                    'condition': 'Ensoleillé'
                }
                return JsonResponse(weather_data)
        
        return JsonResponse({
            'temperature': f"{weather.temperature}°C",
            'humidity': f"{weather.humidity}%",
            'wind_speed': f"{weather.wind_speed} km/h",
            'rain_chance': f"{weather.rain_chance}%",
            'visibility': f"{weather.visibility} km",
            'condition': weather.condition
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def weather_dashboard(request):
   
    regions = WeatherData.objects.values('region').distinct()
    recent_weather = WeatherData.objects.filter(is_current=True).order_by('-recorded_at')[:10]
    
    context = {
        'regions': regions,
        'recent_weather': recent_weather,
    }
    return render(request, 'weather/dashboard.html', context)