"""
    Módulo com abstrações dos objetos vindos de build() do Google API Client.
"""

from typing import Protocol, Any, TypeVar

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class GoogleHttpRequest(Protocol[T]):
    """Abstrai o objeto de requisição do Google antes do disparo."""
    def execute(self) -> T:
        """ Executa a requisição do Google API. """

# Versão "crua" da requisição do Google API.
GoogleRawHttpRequest = GoogleHttpRequest[dict[str, Any]]

class _GoogleResource(Protocol[T]):
    """Abstrai um recurso de um serviço do Google API."""

class GoogleResourceGet(_GoogleResource[T]):
    """Abstrai o método get de um recurso do Google API."""
    def get(self, **kwargs: Any) -> GoogleHttpRequest[T]:
        """ Retorna um objeto de requisição do Google API. """

class GoogleResourceList(_GoogleResource[T]):
    """Abstrai o método list de um recurso do Google API."""
    def list(self, **kwargs: Any) -> GoogleHttpRequest[T]:
        """ Retorna um objeto de requisição do Google API. """

class GoogleService(Protocol):
    """ Abstrai um serviço do Google API. """

def make_request_proxy(request: GoogleRawHttpRequest, model: type[T]) -> GoogleHttpRequest[T]:
    """Cria um proxy para o objeto de requisição do Google API."""
    class _RequestProxy(GoogleHttpRequest[T]):
        def __init__(self, request: GoogleRawHttpRequest, model: type[T]):
            super().__init__()
            self._request = request
            self._model = model

        def execute(self) -> T:
            return self._model.model_validate(self._request.execute())
    return _RequestProxy(request, model)
