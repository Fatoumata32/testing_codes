from django.db import models
from django.conf import settings

class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)  # Add this
    language = models.CharField(max_length=10, default='fr')  # Add this
    session_id = models.CharField(max_length=100, blank=True, null=True)  # Add this
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}"