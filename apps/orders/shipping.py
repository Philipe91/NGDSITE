import requests
import logging
from decimal import Decimal
from django.conf import settings
from .models import ShippingConfig

logger = logging.getLogger(__name__)

def get_shipping_options(cep: str, cart) -> list[dict]:
    """
    Retorna as opções de frete baseadas na configuração do Admin:
    Se Token do Melhor Envio existir => Bate na API oficial
    Senão => Usa regras locais/transportadora fallback
    """
    cep_clean = cep.replace('-', '').strip()
    store_address = getattr(settings, 'STORE_ADDRESS', 'Consultar endereço pelo WhatsApp')
    
    # Busca configurações (singleton)
    config = ShippingConfig.get_solo()

    options = [{
        'id': 'Retirada na Loja',
        'label': 'Retirada na Loja',
        'description': store_address,
        'cost': Decimal('0.00'),
        'days': 'Pronto p/ Retirada',
    }]

    if not cep_clean or len(cep_clean) != 8:
        return options

    # Prepara dimensoes e produtos do carrinho
    total_weight = Decimal('0.00')
    total_volume_cm3 = Decimal('0.00')
    total_value = Decimal('0.00')
    max_length = Decimal('0.00')
    
    me_products = [] # Para Melhor Envio

    for item in cart:
        qtd = int(item['quantity'])
        var = item['variant']
        peso = Decimal(str(var.weight_kg))
        comp = Decimal(str(var.length_cm))
        larg = Decimal(str(var.width_cm))
        alt = Decimal(str(var.height_cm))
        
        total_weight += (peso * qtd)
        total_volume_cm3 += (comp * larg * alt * qtd)
        total_value += (Decimal(str(item['price'])) * qtd)
        max_length = max(max_length, comp, larg, alt)

        # Formato esperado pelo Melhor Envio
        me_products.append({
            "id": str(var.id),
            "width": float(larg),
            "height": float(alt),
            "length": float(comp),
            "weight": float(peso),
            "insurance_value": float(item['price']),
            "quantity": qtd
        })

    # 1. MELHOR ENVIO
    if config.melhor_envio_token:
        try:
            domain = "sandbox.melhorenvio.com.br" if config.is_sandbox else "www.melhorenvio.com.br"
            url = f"https://{domain}/api/v2/me/shipment/calculate"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {config.melhor_envio_token.strip()}"
            }
            payload = {
                "from": {"postal_code": config.cep_origem.replace('-', '')},
                "to": {"postal_code": cep_clean},
                "products": me_products
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=8)
            
            if response.status_code == 200:
                data = response.json()
                # A API retorna lista ou dict, dependendo do payload. Se dict, precisamos das chaves
                if isinstance(data, dict):
                    # Às vezes erro retorna como dict
                    if 'error' in data:
                        logger.error(f"Erro Melhor Envio: {data}")
                    data = [] # Força fallback
                
                # Para cada serviço retornado, vamos adicionar nas opções
                for srv in data:
                    if 'error' in srv:
                        continue
                    
                    price = str(srv.get('custom_price', '0.00'))
                    days = int(srv.get('custom_delivery_time', 0)) + config.dias_adicionais
                    name = str(srv.get('name', 'Transportadora'))
                    company = str(srv.get('company', {}).get('name', ''))
                    
                    if Decimal(price) > 0:
                        options.append({
                            'id': f"me_{srv.get('id')}",
                            'label': f"{company} {name}".strip(),
                            'description': f"Entrega em até {days} dias úteis",
                            'cost': Decimal(price),
                            'days': f"{days} dias úteis",
                        })
                
                if len(options) > 1:
                    # Se achou fretes no Melhor Envio, retorna (já inclui retirada).
                    # Adiciona motoboy local se ativo e CEP compatível.
                    if config.enable_local_delivery and cep_clean.startswith(('70','71','72','73')):
                        options.append({
                            'id': 'Motoboy',
                            'label': 'Entrega Local / Motoboy',
                            'description': 'Apenas para ' + config.local_city,
                            'cost': config.local_price,
                            'days': 'Msm dia ou dia seguinte',
                        })
                    return sort_options(options)

        except Exception as e:
            logger.error(f"Falha ao conectar no Melhor Envio: {e}")
            # Continua pro fallback

    # 2. FALLBACK MANUAL / REGRAS LOCAIS
    is_local = False
    # Tenta usar a capital do BD ou prefixo DF como local (70-73) - mock simples
    if cep_clean.startswith(('70','71','72','73')):
        is_local = True

    if config.enable_local_delivery and is_local:
        # Entrega Local (Motoboy/Carreto)
        base_cost = config.local_price
        kg_cost = Decimal('1.50')
        
        cost_moto = base_cost + (total_weight * kg_cost)
        
        # Motoboy: se medida máxima <= 100cm e peso <= 30kg
        if max_length <= 100 and total_weight <= 30:
            options.append({
                'id': 'Motoboy',
                'label': 'Motoboy Express',
                'description': f'Apenas {config.local_city} e Região',
                'cost': cost_moto,
                'days': '1 a 2 dias úteis',
            })
            
        # Carreto Próprio para Locais Grandes
        cost_carreto = Decimal('70.00') + (total_weight * Decimal('0.50'))
        options.append({
            'id': 'Carreto Especial',
            'label': 'Carreto Especial (Itens Grandes)',
            'description': 'Transporte adaptado especializado em PDV',
            'cost': cost_carreto,
            'days': 'A Combinar',
        })
    else:
        # Transportadora Nacional Mock
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
            'days': f'{5 + config.dias_adicionais} a {12 + config.dias_adicionais} dias úteis',
        })

    return sort_options(options)

def sort_options(options):
    # Ordena: Retirada primeiro, dps menor valor
    return sorted(options, key=lambda x: (x['id'] != 'Retirada na Loja', x['cost']))
