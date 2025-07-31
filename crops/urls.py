from django.urls import path
from . import views

app_name = 'crops'

urlpatterns = [
    path('', views.crops_list, name='list'),
    path('<int:crop_id>/', views.crop_detail, name='detail'),
    path('api/tips/<int:crop_id>/', views.get_crop_tips_api, name='tips_api'),
    path('search/', views.crop_search, name='search'),
    ]