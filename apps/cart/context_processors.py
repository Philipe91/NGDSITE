from .cart import Cart

def cart_processor(request):
    """Context processor para injetar o carrinho em todos os templates"""
    return {'cart': Cart(request)}
