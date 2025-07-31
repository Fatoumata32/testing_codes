from django.contrib import admin
from .models import Crop, CropTip

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name_fr', 'name_wo', 'category', 'growing_season', 'is_active', 'created_at')
    list_filter = ('category', 'growing_season', 'is_active')
    search_fields = ('name_fr', 'name_wo', 'scientific_name')
    ordering = ('name_fr',)

@admin.register(CropTip)
class CropTipAdmin(admin.ModelAdmin):
    list_display = ('title_fr', 'crop', 'tip_type', 'priority', 'is_urgent', 'created_by', 'created_at')
    list_filter = ('tip_type', 'priority', 'is_urgent', 'season', 'crop')
    search_fields = ('title_fr', 'title_wo', 'content_fr', 'content_wo')
    ordering = ('-priority', '-created_at')
    raw_id_fields = ('crop', 'created_by')
