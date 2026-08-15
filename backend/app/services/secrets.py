"""
    Módulo de gerenciamento de credenciais e segredos.
"""

import os
from google.oauth2 import service_account

def get_google_credentials(file: str, **kwargs) -> service_account.Credentials:
    """
        Retorna as credenciais do Google a partir de um arquivo de chave de serviço.
    """
    return service_account.Credentials.from_service_account_file(file, **kwargs)

def get_env_variable(name: str, default: str = None, raise_exception: bool = False) -> str:
    """
        Retorna o valor de uma variável de ambiente.
    """
    value = os.environ.get(name, default)
    if raise_exception and value is None:
        raise ValueError(f"Variável de ambiente {name} não encontrada.")
    return value
