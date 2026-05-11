from apps.catalog.models import MegaMenuTotensCard


def totens_processor(request):
    """Cards do megamenu 'Totens PDV' — separados em featured + others.
    O 'featured' é o card com badge='destaque' (ou o 1º se nenhum tiver)."""
    cards = list(
        MegaMenuTotensCard.objects.filter(is_active=True)
        .select_related("product")
        .order_by("order", "id")
    )

    featured = next((c for c in cards if c.badge == "destaque"), None)
    if featured is None and cards:
        featured = cards[0]

    others = [c for c in cards if c is not featured]

    return {
        "mega_totens_cards": cards,
        "mega_totens_featured": featured,
        "mega_totens_others": others,
    }
