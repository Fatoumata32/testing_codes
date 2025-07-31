from django.urls import path
from . import views

app_name = 'farmconnect_app'

from django.urls import include, path

urlpatterns = [
    # autres routes ici
    path('community/', include(('community.urls', 'community'), namespace='community')),
    path('investisseurs/', views.investors_view, name='investors'),
    path('tools/', views.tools_view, name='tools'),
]


urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('investors/', views.investors, name='investors'),
    
]
# farmconnect_app/urls.py - Mise à jour de vos URLs

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'farmconnect_app'

urlpatterns = [
    # Pages principales
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('investors/', views.investors, name='investors'),
    
    # Authentification personnalisée
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('community/', views.community_view, name='community_view'),
    
    # Réinitialisation de mot de passe
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
    
    # Pages utilisateur
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
]

# ===================================
# urls.py principal du projet
# ===================================

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # App principale
    path('', include('farmconnect_app.urls')),
    
    # Autres apps
    path('crops/', include('crops.urls')),
    path('weather/', include('weather.urls')),
    path('community/', include('community.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('chat/', include('chat.urls')),
    path('community/', views.community_view, name='community_view'),
    
    # Authentification Django par défaut (fallback)
    path('accounts/', include('django.contrib.auth.urls')),
]

# Servir les fichiers média en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'farmconnect_app'

urlpatterns = [
    # Page d'accueil
    path('', views.home, name='home'),
    
    # Authentification - URLS SIMPLES SANS RÉCURSION
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    
    # Pages utilisateur
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),

    path('crops/', include('crops.urls')),
    
    # Pages statiques
    path('about/', views.about, name='about'),
    path('investors/', views.investors, name='investors'),
    
    path('community/', views.community, name='community'),
    path('about/', views.about, name='about'),
    path('tools/', views.tools_view, name='tools'),
    
    # Réinitialisation de mot de passe - SIMPLES
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset-done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ), 
         name='password_reset_done'),
]