from django.db import models
from farmconnect_app.models import User

class Crop(models.Model):
    """Modèle pour les différentes cultures"""
    name_fr = models.CharField(max_length=100, verbose_name="Nom en français")
    name_wo = models.CharField(max_length=100, verbose_name="Nom en wolof")
    scientific_name = models.CharField(max_length=100, blank=True, verbose_name="Nom scientifique")
    category = models.CharField(max_length=50, choices=[
        ('cereales', 'Céréales'),
        ('legumineuses', 'Légumineuses'),
        ('legumes', 'Légumes'),
        ('fruits', 'Fruits'),
        ('tubercules', 'Tubercules'),
    ])
    growing_season = models.CharField(max_length=100, verbose_name="Saison de culture")
    planting_period = models.CharField(max_length=100, verbose_name="Période de plantation")
    harvest_period = models.CharField(max_length=100, verbose_name="Période de récolte")
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='crops/', null=True, blank=True)
    description_fr = models.TextField(blank=True)
    description_wo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_fr

    class Meta:
        verbose_name = "Culture"
        verbose_name_plural = "Cultures"
        ordering = ['name_fr']

class CropTip(models.Model):
    """Conseils agricoles pour les cultures"""
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='tips')
    title_fr = models.CharField(max_length=200, verbose_name="Titre en français")
    title_wo = models.CharField(max_length=200, verbose_name="Titre en wolof")
    content_fr = models.TextField(verbose_name="Contenu en français")
    content_wo = models.TextField(verbose_name="Contenu en wolof")
    tip_type = models.CharField(max_length=50, choices=[
        ('planting', 'Plantation'),
        ('care', 'Entretien'),
        ('fertilization', 'Fertilisation'),
        ('irrigation', 'Irrigation'),
        ('pest_control', 'Lutte antiparasitaire'),
        ('harvest', 'Récolte'),
        ('storage', 'Conservation'),
    ])
    season = models.CharField(max_length=50, blank=True)
    is_urgent = models.BooleanField(default=False, verbose_name="Conseil urgent")
    priority = models.IntegerField(default=1, choices=[
        (1, 'Faible'),
        (2, 'Normale'),
        (3, 'Élevée'),
        (4, 'Critique'),
    ])
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', '-created_at']
        verbose_name = "Conseil agricole"
        verbose_name_plural = "Conseils agricoles"

    def __str__(self):
        return f"{self.title_fr} - {self.crop.name_fr}"
