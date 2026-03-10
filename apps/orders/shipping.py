from decimal import Decimal
from django.conf import settings


def get_shipping_options(cep: str) -> list[dict]:
    """
    Retorna as opções de frete disponíveis para o CEP informado.
    MVP: Retirada em loja (gratuita) + Frete Fixo (valor configurável no settings).
    """
    cep_clean = cep.replace('-', '').strip()

    fixed_cost = getattr(settings, 'SHIPPING_FIXED_COST', Decimal('25.00'))
    store_address = getattr(settings, 'STORE_ADDRESS', 'Consultar endereço pelo WhatsApp')

    options = [
        {
            'id': 'retirada',
            'label': 'Retirada na Loja',
            'description': store_address,
            'cost': Decimal('0.00'),
            'days': '—',
        },
        {
            'id': 'frete_fixo',
            'label': 'Entrega / Motoboy',
            'description': f'CEP: {cep_clean}',
            'cost': Decimal(str(fixed_cost)),
            'days': 'Combinar',
        },
    ]

    return options
