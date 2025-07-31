from django.db import models

class WeatherData(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    region = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_current = models.BooleanField(default=True)  # Add this field
    
    def __str__(self):
        return f"Weather at {self.location} - {self.timestamp}"