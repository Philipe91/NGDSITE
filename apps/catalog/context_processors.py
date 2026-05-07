from apps.catalog.models import Product, Category

def totens_processor(request):
    try:
        cat = Category.objects.get(slug='totens-pdv')
        totens = list(
            Product.objects.filter(category=cat, is_active=True, name__istartswith="Totem")
            .order_by("id")[:6]
        )
    except Category.DoesNotExist:
        totens = []

    by_slug = {p.slug: p for p in totens}

    return {
        "mega_totens": totens,
        "mega_totem_triangular": by_slug.get("totem-triangular"),
        "mega_totem_triedro": by_slug.get("totem-triedro-em-poliondas"),
    }
