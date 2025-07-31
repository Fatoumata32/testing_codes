from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
import json
import random

def chat_interface(request):
    if request.user.is_authenticated:
        recent_messages = ChatMessage.objects.filter(
            user=request.user
        ).order_by('-timestamp')[:10]
    else:
        recent_messages = []
    
    return render(request, 'chat/interface.html', {'recent_messages': recent_messages})

@csrf_exempt
def chat_message_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            language = data.get('language', 'fr')
            
            # Réponses simples basées sur des règles
            responses_fr = [
                "Excellente question ! Pour améliorer vos rendements, je recommande d'analyser votre sol et d'adapter votre fertilisation.",
                "Pendant la saison sèche, concentrez-vous sur l'irrigation goutte à goutte et le paillage pour conserver l'humidité.",
                "Les rotations culturales sont essentielles ! Alternez entre légumineuses et céréales pour maintenir la fertilité du sol.",
                "Pour lutter contre les parasites naturellement, utilisez des extraits de neem ou installez des pièges à phéromones.",
                "Consultez les prévisions météo régulièrement pour optimiser vos activités agricoles.",
                "N'hésitez pas à rejoindre notre communauté d'agriculteurs pour partager vos expériences."
            ]
            
            responses_wo = [
                "Làkk bu baax laa ! Ngir baax sa njuumte, xam sa suuf te jël alkaati yu am solo.",
                "Ci jamono bu reer, jëfandikoo arrosage goutte à goutte ak paillage ngir sukkandiku ndaw.",
                "Soppalel mburu yi baax na ! Weccal légumineuses ak céréales ngir suuf si dugg baax.",
                "Ngir xeex ak yàkkar yu baax, jëfandikoo neem walla yor piège à phéromones.",
                "Xool taw yi rek rek ngir baax sa liggéey yu jëmm.",
                "Duggal ci réew mi jëmmkat yo ngir wax sa xalaat ak jàng ku leen."
            ]
            
            responses = responses_fr if language == 'fr' else responses_wo
            response = random.choice(responses)
            
            # Sauvegarder le message si l'utilisateur est connecté
            if request.user.is_authenticated:
                ChatMessage.objects.create(
                    user=request.user,
                    message=message,
                    response=response,
                    language=language,
                    session_id=request.session.session_key or 'anonymous'
                )
            
            return JsonResponse({'response': response})
            
        except Exception as e:
            return JsonResponse({'error': 'Erreur lors du traitement du message'}, status=500)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@login_required
def chat_history(request):
    messages = ChatMessage.objects.filter(user=request.user).order_by('-timestamp')[:50]
    return render(request, 'chat/history.html', {'messages': messages})