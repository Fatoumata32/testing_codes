from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informations FarmConnect', {
            'fields': ('role', 'phone_number', 'region', 'village', 'farm_size', 
                      'preferred_language', 'profile_picture', 'is_verified', 'birth_date')
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'region', 'is_verified', 'date_joined')
    list_filter = ('role', 'region', 'is_verified', 'preferred_language', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'region', 'village')
    ordering = ('-date_joined',)
