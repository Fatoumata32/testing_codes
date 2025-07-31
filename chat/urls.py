from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_interface, name='interface'),
    path('api/message/', views.chat_message_api, name='message_api'),
    path('history/', views.chat_history, name='history'),
]