"""Validadores de CPF e CNPJ (dígitos verificadores) — sem dependência externa."""
import re
from django.core.exceptions import ValidationError


def _so_digitos(valor: str) -> str:
    return re.sub(r'\D', '', valor or '')


def valida_cpf(valor: str):
    cpf = _so_digitos(valor)
    if len(cpf) != 11:
        raise ValidationError("CPF deve ter 11 dígitos.")
    if cpf == cpf[0] * 11:
        raise ValidationError("CPF inválido.")
    # 1º dígito
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10 % 11) % 10
    # 2º dígito
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10 % 11) % 10
    if d1 != int(cpf[9]) or d2 != int(cpf[10]):
        raise ValidationError("CPF inválido. Confira os números digitados.")


def valida_cnpj(valor: str):
    cnpj = _so_digitos(valor)
    if len(cnpj) != 14:
        raise ValidationError("CNPJ deve ter 14 dígitos.")
    if cnpj == cnpj[0] * 14:
        raise ValidationError("CNPJ inválido.")
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
    d1 = soma % 11
    d1 = 0 if d1 < 2 else 11 - d1
    soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
    d2 = soma % 11
    d2 = 0 if d2 < 2 else 11 - d2
    if d1 != int(cnpj[12]) or d2 != int(cnpj[13]):
        raise ValidationError("CNPJ inválido. Confira os números digitados.")


def valida_documento(tipo_pessoa: str, valor: str):
    """Valida CPF (PF) ou CNPJ (PJ) conforme o tipo de pessoa."""
    if tipo_pessoa == 'PJ':
        valida_cnpj(valor)
    else:
        valida_cpf(valor)
