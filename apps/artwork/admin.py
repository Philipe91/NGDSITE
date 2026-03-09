from django.contrib import admin
from .models import ArtworkFile


@admin.register(ArtworkFile)
class ArtworkFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'original_name', 'uploaded_at']
    list_filter = ['uploaded_at']
    readonly_fields = ['original_name', 'uploaded_at']
    raw_id_fields = ['order']
