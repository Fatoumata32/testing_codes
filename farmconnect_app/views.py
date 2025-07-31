# farmconnect_app/views.py - VERSION CORRIGÉE SANS ERREUR DE SYNTAXE

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.cache import never_cache
from django.utils.translation import gettext as _
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q, Count
from .models import User
import json
import logging
import re

# Configuration du logging pour debug
logger = logging.getLogger(__name__)

def home(request):
    """Page d'accueil avec gestion sécurisée des imports"""
    
    # Calcul sécurisé des totaux
    total_farmers = User.objects.filter(role='farmer').count()
    total_crops = 50  # Valeur par défaut
    
    context = {
        'total_farmers': total_farmers,
        'total_crops': total_crops,
        'recent_tips': [],
        'recent_posts': [],
        'weather_data': None,
        'crops': [],
    }
    return render(request, 'farmconnect_app/home.html', context)

@csrf_protect
@never_cache
def custom_login(request):
    """Vue de connexion personnalisée avec debug"""
    
    print(f"DEBUG: Login view called with method: {request.method}")
    
    if request.user.is_authenticated:
        print("DEBUG: User already authenticated, redirecting to dashboard")
        return redirect('farmconnect_app:dashboard')
    
    if request.method == 'POST':
        print("DEBUG: Processing POST request for login")
        
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me')
        
        print(f"DEBUG: Username: {username}, Password length: {len(password) if password else 0}")
        
        if not username or not password:
            print("DEBUG: Missing username or password")
            messages.error(request, _('Veuillez remplir tous les champs.'))
            return render(request, 'registration/login.html')
        
        # Tentative d'authentification
        print(f"DEBUG: Attempting authentication for user: {username}")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print(f"DEBUG: Authentication successful for user: {user.username}")
            if user.is_active:
                print("DEBUG: User is active, logging in")
                login(request, user)
                
                # Gestion du "Se souvenir de moi"
                if not remember_me:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(1209600)  # 2 semaines
                
                messages.success(request, _('Connexion réussie ! Bienvenue {}').format(user.get_full_name() or user.username))
                
                # Redirection
                redirect_to = request.GET.get('next', reverse('farmconnect_app:dashboard'))
                print(f"DEBUG: Redirecting to: {redirect_to}")
                return HttpResponseRedirect(redirect_to)
            else:
                print("DEBUG: User account is inactive")
                messages.error(request, _('Votre compte est désactivé. Contactez l\'administrateur.'))
        else:
            print("DEBUG: Authentication failed")
            messages.error(request, _('Identifiant ou mot de passe incorrect.'))
    
    # GET request ou erreur de POST
    form = AuthenticationForm()
    redirect_to = request.GET.get('next', reverse('farmconnect_app:dashboard'))
    
    context = {
        'form': form,
        'redirect_field_name': 'next',
        'redirect_field_value': redirect_to,
    }
    
    print("DEBUG: Rendering login template")
    return render(request, 'registration/login.html', context)

def custom_logout(request):
    """Vue de déconnexion personnalisée"""
    
    if request.user.is_authenticated:
        user_name = request.user.get_full_name() or request.user.username
        logout(request)
        messages.success(request, _('Vous avez été déconnecté avec succès. À bientôt {}!').format(user_name))
    
    return redirect('farmconnect_app:home')

def register(request):
    """Vue d'inscription avec debug - Adaptée au modèle User"""
    
    print(f"DEBUG: Register view called with method: {request.method}")
    
    if request.user.is_authenticated:
        print("DEBUG: User already authenticated, redirecting to dashboard")
        return redirect('farmconnect_app:dashboard')
        
    if request.method == 'POST':
        print("DEBUG: Processing POST request for registration")
        print(f"DEBUG: POST data keys: {list(request.POST.keys())}")
        
        try:
            data = request.POST
            
            # Debug des données reçues
            first_name = data.get('first_name', '').strip()
            last_name = data.get('last_name', '').strip()
            phone_number = data.get('phone_number', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '')
            confirm_password = data.get('confirm_password', '')
            region = data.get('region', '').strip()
            village = data.get('village', '').strip()
            language = data.get('language', 'fr')
            role = data.get('role', 'farmer')
            
            print(f"DEBUG: Parsed data - Name: {first_name} {last_name}, Phone: {phone_number}")
            
            # Validation des champs requis
            required_fields = {
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone_number,
                'password': password
            }
            
            missing_fields = [field for field, value in required_fields.items() if not value]
            
            if missing_fields:
                print(f"DEBUG: Missing required fields: {missing_fields}")
                messages.error(request, _('Les champs suivants sont requis: {}').format(', '.join(missing_fields)))
                return render(request, 'registration/register.html')
            
            # Vérification du mot de passe confirmé (si présent)
            if confirm_password and password != confirm_password:
                print("DEBUG: Password confirmation mismatch")
                messages.error(request, _('Les mots de passe ne correspondent pas.'))
                return render(request, 'registration/register.html')
            
            # Nettoyage et validation du numéro de téléphone selon votre modèle
            phone_clean = phone_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            
            # Formatage selon le regex de votre modèle: +221XXXXXXXXX
            if not phone_clean.startswith('+221'):
                if phone_clean.startswith('221'):
                    phone_clean = '+' + phone_clean
                elif phone_clean.startswith('77') or phone_clean.startswith('78') or phone_clean.startswith('76') or phone_clean.startswith('70'):
                    # Numéros sénégalais typiques
                    phone_clean = '+221' + phone_clean
                else:
                    # Essayer d'ajouter +221 par défaut
                    phone_clean = '+221' + phone_clean.lstrip('0')
            
            print(f"DEBUG: Cleaned phone number: {phone_clean}")
            
            # Validation du format avec le regex de votre modèle
            phone_regex = r'^\+221\d{9}$'
            if not re.match(phone_regex, phone_clean):
                print(f"DEBUG: Phone number format invalid: {phone_clean}")
                messages.error(request, _('Format de numéro invalide. Utilisez le format: +221XXXXXXXXX'))
                return render(request, 'registration/register.html')
            
            # Vérification de l'unicité du numéro de téléphone
            if User.objects.filter(Q(username=phone_clean) | Q(phone_number=phone_clean)).exists():
                print("DEBUG: Phone number already exists")
                messages.error(request, _('Ce numéro de téléphone est déjà utilisé.'))
                return render(request, 'registration/register.html')
            
            # Validation du rôle selon vos choix
            valid_roles = ['farmer', 'agent', 'admin']
            if role not in valid_roles:
                role = 'farmer'  # Valeur par défaut
            
            # Validation de la langue selon vos choix
            valid_languages = ['fr', 'wo']
            if language not in valid_languages:
                language = 'fr'  # Valeur par défaut
            
            print(f"DEBUG: Creating user with role: {role}, language: {language}")
            
            # Création de l'utilisateur
            print("DEBUG: Creating new user")
            user = User.objects.create_user(
                username=phone_clean,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_clean,
                region=region,
                village=village,
                preferred_language=language,
                role=role
            )
            
            print(f"DEBUG: User created successfully with ID: {user.id}")
            
            # Connexion automatique
            login(request, user)
            print("DEBUG: User logged in automatically")
            
            messages.success(request, _('Inscription réussie ! Bienvenue sur FarmConnect Senegal, {}.').format(user.get_full_name()))
            return redirect('farmconnect_app:dashboard')
            
        except Exception as e:
            print(f"DEBUG: Registration error: {str(e)}")
            logger.error(f"Registration error: {str(e)}")
            messages.error(request, _('Erreur lors de l\'inscription: {}').format(str(e)))
    
    print("DEBUG: Rendering registration template")
    return render(request, 'registration/register.html')

@login_required
def dashboard(request):
    """Vue du tableau de bord utilisateur"""
    
    print(f"DEBUG: Dashboard view called for user: {request.user.username}")
    
    user = request.user
    
    # Vérifier si c'est la première connexion
    if not user.last_login or user.created_at == user.last_login:
        messages.info(request, _('Bienvenue sur FarmConnect ! Découvrez toutes nos fonctionnalités.'))
    
    context = {
        'weather_data': None,
        'recent_tips': [],
        'my_posts': [],
        'my_products': [],
        'favorite_crops': [],
        'user': user,
    }
    
    return render(request, 'farmconnect_app/dashboard.html', context)

@login_required
def profile(request):
    """Vue du profil utilisateur - Adaptée au modèle User"""
    
    if request.method == 'POST':
        user = request.user
        
        # Mise à jour des champs de base
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.region = request.POST.get('region', user.region)
        user.village = request.POST.get('village', user.village)
        user.preferred_language = request.POST.get('preferred_language', user.preferred_language)
        
        # Mise à jour de la taille de l'exploitation
        farm_size = request.POST.get('farm_size')
        if farm_size:
            try:
                user.farm_size = float(farm_size)
            except ValueError:
                user.farm_size = None
        else:
            user.farm_size = None
        
        # Mise à jour de la date de naissance
        birth_date = request.POST.get('birth_date')
        if birth_date:
            from datetime import datetime
            try:
                user.birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
            except ValueError:
                user.birth_date = None
        
        # Gestion de l'upload de photo de profil
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        # Le rôle ne peut être modifié que par un admin
        if request.user.is_superuser or request.user.role == 'admin':
            new_role = request.POST.get('role')
            if new_role in ['farmer', 'agent', 'admin']:
                user.role = new_role
        
        user.save()
        messages.success(request, _('Profil mis à jour avec succès.'))
        return redirect('farmconnect_app:profile')
    
    return render(request, 'farmconnect_app/profile.html')

def about(request):
    """Page à propos"""
    return render(request, 'farmconnect_app/about.html')

def investors(request):
    """Page investisseurs"""
    stats = {
        'total_users': User.objects.count(),
        'active_farmers': User.objects.filter(role='farmer', is_active=True).count(),
        'regions_covered': User.objects.values('region').distinct().count(),
        'crops_supported': 50,  # Valeur par défaut
    }
    
    return render(request, 'farmconnect_app/investors.html', {'stats': stats})

def password_reset_request(request):
    """Vue pour demander une réinitialisation de mot de passe"""
    
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            try:
                user = User.objects.get(username=username)
                messages.success(request, _('Un lien de réinitialisation sera envoyé si ce compte existe.'))
            except User.DoesNotExist:
                messages.success(request, _('Un lien de réinitialisation sera envoyé si ce compte existe.'))
        else:
            messages.error(request, _('Veuillez saisir votre identifiant.'))
    
    return render(request, 'registration/password_reset.html')

def debug_view(request):
    """Vue de debug pour tester la configuration"""
    
    context = {
        'user_authenticated': request.user.is_authenticated,
        'user_info': str(request.user) if request.user.is_authenticated else 'Anonymous',
        'session_keys': list(request.session.keys()),
        'post_data': dict(request.POST) if request.method == 'POST' else {},
        'get_data': dict(request.GET),
        'total_users': User.objects.count(),
    }
    
    return render(request, 'farmconnect_app/debug.html', context)