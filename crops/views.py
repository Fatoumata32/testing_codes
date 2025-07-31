from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Crop, CropTip

def crops_list(request):
    crops = Crop.objects.filter(is_active=True).order_by('name_fr')
    recent_tips = CropTip.objects.select_related('crop').order_by('-created_at')[:10]
    
    context = {
        'crops': crops,
        'recent_tips': recent_tips,
    }
    return render(request, 'crops/list.html', context)

def crop_detail(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    tips = CropTip.objects.filter(crop=crop).order_by('-priority', '-created_at')
    
    context = {
        'crop': crop,
        'tips': tips,
    }
    return render(request, 'crops/detail.html', context)

def get_crop_tips_api(request, crop_id):
    language = request.GET.get('lang', 'fr')
    
    try:
        crop = Crop.objects.get(id=crop_id)
        tips = CropTip.objects.filter(crop=crop).order_by('-priority', '-created_at')
        
        tips_data = []
        for tip in tips:
            tips_data.append({
                'title': tip.title_fr if language == 'fr' else tip.title_wo,
                'content': tip.content_fr if language == 'fr' else tip.content_wo,
                'type': tip.tip_type,
                'urgent': tip.is_urgent,
                'priority': tip.priority
            })
        
        return JsonResponse({'tips': tips_data})
    
    except Crop.DoesNotExist:
        return JsonResponse({'error': 'Culture non trouvée'}, status=404)

def crop_search(request):
    query = request.GET.get('q', '')
    if query:
        crops = Crop.objects.filter(
            Q(name_fr__icontains=query) | Q(name_wo__icontains=query)
        ).filter(is_active=True)
    else:
        crops = Crop.objects.filter(is_active=True)
    
    return render(request, 'crops/search.html', {'crops': crops, 'query': query})

# crops/views.py (créez ces vues si elles n'existent pas)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def crop_list(request):
    """Liste des cultures et conseils agricoles"""
    context = {
        'crops': [],  # À remplacer par vos données
        'tips': [],   # À remplacer par vos conseils
    }
    return render(request, 'crops/list.html', context)

@login_required
def crop_detail(request, crop_id):
    """Détail d'une culture spécifique"""
    context = {
        'crop_id': crop_id,
    }
    return render(request, 'crops/detail.html', context)

@login_required
def farming_tips(request):
    """Conseils agricoles"""
    context = {
        'tips': [],
    }
    return render(request, 'crops/tips.html', context)

@login_required
def farming_calendar(request):
    """Calendrier agricole"""
    context = {
        'calendar_data': {},
    }
    return render(request, 'crops/calendar.html', context)
