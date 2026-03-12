from decimal import Decimal
from django.conf import settings

def get_shipping_options(cep: str, cart) -> list[dict]:
    """
    Retorna as opções de frete dinâmico baseado no peso e volume real das variantes.
    """
    cep_clean = cep.replace('-', '').strip()
    store_address = getattr(settings, 'STORE_ADDRESS', 'Consultar endereço pelo WhatsApp')

    options = [{
        'id': 'Retirada na Loja',
        'label': 'Retirada na Loja',
        'description': store_address,
        'cost': Decimal('0.00'),
        'days': '—',
    }]

    if not cep_clean or len(cep_clean) != 8:
        return options

    # 1. Dimensão Cúbica e Peso do Carrinho
    total_weight = Decimal('0.00')
    total_volume_cm3 = Decimal('0.00')
    max_length = Decimal('0.00')
    
    for item in cart:
        qtd = Decimal(str(item['quantity']))
        var = item['variant']
        peso = Decimal(str(var.weight_kg))
        comp = Decimal(str(var.length_cm))
        larg = Decimal(str(var.width_cm))
        alt = Decimal(str(var.height_cm))
        
        total_weight += (peso * qtd)
        total_volume_cm3 += (comp * larg * alt * qtd)
        max_length = max(max_length, comp, larg, alt)

    # 2. Base Estimada por Região (Baseado no 1º dígito do CEP)
    # Brasilia: CEPs começam com 70, 71, 72, 73
    is_local = cep_clean.startswith(('70','71','72','73'))

    # Custo de Transporte (Base):
    if is_local:
        # Entrega Local (Motoboy/Carreto)
        base_cost = Decimal('25.00')
        kg_cost = Decimal('1.50')
        
        cost_moto = base_cost + (total_weight * kg_cost)
        
        # Motoboy: se medida máxima <= 100cm e peso <= 30kg
        if max_length <= 100 and total_weight <= 30:
            options.append({
                'id': 'Motoboy',
                'label': 'Motoboy Express',
                'description': f'Apenas Brasília e Região (Total: {total_weight:.1f}kg)',
                'cost': cost_moto,
                'days': '1 a 2 dias úteis',
            })
            
        # Carreto Próprio para Locais ou Grandes
        cost_carreto = Decimal('70.00') + (total_weight * Decimal('0.50'))
        options.append({
            'id': 'Carreto Especial',
            'label': 'Carreto Especial (Itens Grandes)',
            'description': 'Transporte adaptado especializado em PDV',
            'cost': cost_carreto,
            'days': 'A Combinar',
        })
    else:
        # Transportadora Nacional (Simulação JadLog/Braspress)
        base_nacional = Decimal('65.00')
        kg_adicional = Decimal('4.50')
        
        regiao_cod = int(cep_clean[0])
        fator_regiao = Decimal('1.0')
        if regiao_cod in [0,1,2,3]: fator_regiao = Decimal('1.2') # SP/RJ/MG
        elif regiao_cod in [4,5,6]: fator_regiao = Decimal('2.0') # NE/N
        elif regiao_cod in [8,9]: fator_regiao = Decimal('1.8')   # Sul
        
        cubagem_kg = total_volume_cm3 / Decimal('6000') # Rodoviário Padrão
        peso_taxado = max(total_weight, cubagem_kg)
        
        cost_transp = (base_nacional + (peso_taxado * kg_adicional)) * fator_regiao
        
        options.append({
            'id': 'Transportadora Rodoviária',
            'label': 'Transportadora Especializada',
            'description': f'Baseado em {peso_taxado:.1f}kg (Cálculo Cubado)',
            'cost': cost_transp,
            'days': '5 a 12 dias úteis',
        })

    return options
