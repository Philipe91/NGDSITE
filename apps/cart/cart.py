from decimal import Decimal
from django.conf import settings
from apps.catalog.models import ProductVariant

class Cart:
    def __init__(self, request):
        """Inicializa o carrinho via Sessão"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, variant, quantity=1, update_quantity=False):
        """Adiciona variante ao carrinho ou atualiza quantidade."""
        variant_id = str(variant.id)
        if variant_id not in self.cart:
            self.cart[variant_id] = {'quantity': 0, 'price': str(variant.price)}
        if update_quantity:
            self.cart[variant_id]['quantity'] = quantity
        else:
            self.cart[variant_id]['quantity'] += quantity
            
        self.save()

    def update_price(self, variant, custom_price):
        """Atualiza o preco customizado no carrinho"""
        variant_id = str(variant.id)
        if variant_id in self.cart:
            self.cart[variant_id]['price'] = str(custom_price)
            self.save()

    def save(self):
        # marca a sessão como modificada
        self.session.modified = True

    def remove(self, variant):
        """Remove variante do carrinho"""
        variant_id = str(variant.id)
        if variant_id in self.cart:
            del self.cart[variant_id]
            self.save()

    def __iter__(self):
        """Itera sobre os itens carregando do banco de dados quando necessário"""
        import copy
        
        variant_ids = self.cart.keys()
        variants = ProductVariant.objects.filter(id__in=variant_ids).select_related('product')
        
        # Faz uma cópia profunda para não sujar o self.cart com objetos complexos
        cart_copy = copy.deepcopy(self.cart)
        for variant in variants:
            cart_copy[str(variant.id)]['variant'] = variant
            
        for item in cart_copy.values():
            item['price'] = Decimal(str(item['price']))
            item['total_price'] = item['price'] * int(item['quantity'])
            yield item

    def __len__(self):
        """Conta quantos itens físicos existem no carrinho no total"""
        return sum(item['quantity'] for item in self.cart.values())
        
    def count(self):
        """Alternative len to easily fetch count without len scope limits."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Esvazia o carrinho"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
