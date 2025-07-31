from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from crops.models import Crop, CropTip
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with initial data for FarmConnect Senegal'
ECHO is off.
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🌱 Initialisation des données FarmConnect Senegal...'))
ECHO is off.
        # Create admin user if doesn't exist
        self.create_admin_user()
ECHO is off.
        # Create crops
        self.create_crops()
ECHO is off.
        # Create sample farmers
        self.create_sample_users()
ECHO is off.
        # Create tips
        self.create_crop_tips()
ECHO is off.
        self.stdout.write(self.style.SUCCESS('✅ Données initialisées avec succès!'))
ECHO is off.
    def create_admin_user(self):
        if not User.objects.filter(is_superuser=True).exists():
            admin = User.objects.create_user(
                username='admin',
                email='admin@farmconnect.sn',
                password='admin123',
                first_name='Administrateur',
                last_name='FarmConnect',
                phone_number='+221771234567',
                role='admin',
                is_staff=True,
                is_superuser=True,
                is_verified=True
            )
            self.stdout.write(f'Admin créé: {admin.username} / admin123')
ECHO is off.
    def create_crops(self):
        crops_data = [
            {
                'name_fr': 'Mil', 'name_wo': 'Souna', 
                'category': 'cereales', 'growing_season': 'Hivernage',
                'planting_period': 'Juin-Juillet', 'harvest_period': 'Octobre-Novembre'
            },
            {
                'name_fr': 'Maïs', 'name_wo': 'Mburu jaaw', 
                'category': 'cereales', 'growing_season': 'Hivernage',
                'planting_period': 'Mai-Juillet', 'harvest_period': 'Septembre-Octobre'
            },
            {
                'name_fr': 'Riz', 'name_wo': 'Ceeb', 
                'category': 'cereales', 'growing_season': 'Hivernage',
                'planting_period': 'Juin-Août', 'harvest_period': 'Novembre-Décembre'
            },
            {
                'name_fr': 'Arachide', 'name_wo': 'Gerte', 
                'category': 'legumineuses', 'growing_season': 'Hivernage',
                'planting_period': 'Juin-Juillet', 'harvest_period': 'Octobre-Novembre'
            },
            {
                'name_fr': 'Tomate', 'name_wo': 'Xoñ', 
                'category': 'legumes', 'growing_season': 'Saison sèche',
                'planting_period': 'Octobre-Décembre', 'harvest_period': 'Janvier-Mars'
            },
        ]
ECHO is off.
        for crop_data in crops_data:
            crop, created = Crop.objects.get_or_create(
                name_fr=crop_data['name_fr'],
                defaults=crop_data
            )
            if created:
                self.stdout.write(f'Culture créée: {crop.name_fr}')
ECHO is off.
    def create_sample_users(self):
        sample_users = [
            {
                'username': '+221771111111', 'phone_number': '+221771111111',
                'first_name': 'Amadou', 'last_name': 'Diallo',
                'region': 'Thiès', 'village': 'Keur Moussa', 'role': 'farmer'
            },
            {
                'username': '+221772222222', 'phone_number': '+221772222222',
                'first_name': 'Fatou', 'last_name': 'Sow',
                'region': 'Kaolack', 'village': 'Kahone', 'role': 'farmer'
            },
        ]
ECHO is off.
        for user_data in sample_users:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    password='farmer123',
                    email=f"{user_data['first_name'].lower^(^)}@farmconnect.sn",
                    farm_size=random.uniform(0.5, 5.0),
                    is_verified=True,
                    **user_data
                )
                self.stdout.write(f'Utilisateur créé: {user.get_full_name()}')
ECHO is off.
    def create_crop_tips(self):
        crops = Crop.objects.all()
        admin_user = User.objects.filter(role='admin').first()
ECHO is off.
        for crop in crops:
            CropTip.objects.get_or_create(
                crop=crop,
                title_fr=f'Conseils pour {crop.name_fr}',
                defaults={
                    'title_wo': f'Waxtaan ngir {crop.name_wo}',
                    'content_fr': f'Conseils pratiques pour cultiver le {crop.name_fr} au Sénégal.',
                    'content_wo': f'Waxtaan yu baax ngir weccal {crop.name_wo} ci Senegaal.',
                    'tip_type': 'planting',
                    'created_by': admin_user,
                    'priority': 2
                }
            )
        self.stdout.write('Conseils créés')
