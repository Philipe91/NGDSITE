from .models import SEOConfig

def seo_settings(request):
    return {
        'seo': SEOConfig.get_solo()
    }
