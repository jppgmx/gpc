"""
    Módulo de gerenciamento de credenciais e segredos.
"""

from google.oauth2 import service_account

def get_google_credentials(file: str, **kwargs) -> service_account.Credentials:
    """
        Retorna as credenciais do Google a partir de um arquivo de chave de serviço.
    """
    return service_account.Credentials.from_service_account_file(file, **kwargs)
