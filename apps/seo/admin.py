from django.contrib import admin
from .models import SEOConfig

@admin.register(SEOConfig)
class SEOConfigAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'meta_title_default')
    
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True
