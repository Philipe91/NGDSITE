from django.conf import settings
from django.shortcuts import get_object_or_404, render
from .models import Product, Category

def home(request):
    categories = Category.objects.filter(is_active=True)
    if settings.PORTFOLIO_MODE:
        # Vitrine: a home é o catálogo inteiro, não só os destaques
        featured_products = Product.objects.filter(is_active=True)
    else:
        featured_products = Product.objects.filter(is_active=True, is_featured=True)
        if not featured_products:
            featured_products = Product.objects.filter(is_active=True)

    context = {
        'categories': categories,
        'featured_products': featured_products,
        'catalogo_cards': monta_cards_do_catalogo(
            featured_products,
            fotos_por_produto=3 if settings.PORTFOLIO_MODE else 1,
        ),
    }
    return render(request, 'catalog/home.html', context)


def monta_cards_do_catalogo(produtos, fotos_por_produto=3):
    """Monta os cards da vitrine repetindo cada produto com fotos diferentes.

    A repeticao vai em rodadas: primeiro a capa de todos os produtos, depois a
    segunda foto de todos, e assim por diante. Assim o mesmo produto nunca
    aparece em cards vizinhos, e o catalogo ganha volume mostrando aplicacoes
    diferentes da mesma peca.
    """
    fotos = {}
    for produto in produtos:
        vistas, lista = set(), []
        candidatas = []
        if produto.featured_image:
            candidatas.append(produto.featured_image)
        candidatas += [img.image for img in produto.images.all()]
        for foto in candidatas:
            if not foto or foto.name in vistas:
                continue
            vistas.add(foto.name)
            lista.append(foto)
            if len(lista) >= fotos_por_produto:
                break
        fotos[produto.pk] = lista

    cards = []
    for rodada in range(fotos_por_produto):
        for produto in produtos:
            lista = fotos.get(produto.pk) or []
            if rodada < len(lista):
                cards.append({'produto': produto, 'imagem': lista[rodada]})
    return cards

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = category.products.filter(is_active=True)
    # Totens PDV: exibir apenas produtos cujo nome começa com "Totem"
    # (Wobbler, Faixa de Gôndola e Lixeira estão na mesma categoria por legado,
    #  mas têm página própria via nav direto no header.)
    if slug == 'totens-pdv':
        products = products.filter(name__istartswith='Totem')
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'catalog/category_detail.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    variants = product.variants.filter(is_active=True).order_by('price')
    images = product.images.all()
    
    context = {
        'product': product,
        'variants': variants,
        'images': images,
    }
    return render(request, 'catalog/product_detail.html', context)
