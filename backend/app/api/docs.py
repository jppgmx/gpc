"""
    API de documentos
"""

from logging import getLogger

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from services.data_store import DataStore
from services.document_provider import DocumentProvider
from models.sources.url import URLSource
from models.sources.cache import CacheSource
from models.transformers.html_transformer import ContentHTMLTransformer
from models.transformers.markdown import HTML2MarkdownTransformer
from models.mdconvs.privacy import PrivacyNormalizer

router = APIRouter()
data_store = DataStore()
provider = DocumentProvider(data_store=data_store)
LOGGER = getLogger(__name__)

data_store.allocate_dir("docs")

# Documento 'terms' - Termos e Condições do Codeforces
provider.add_source(
    source=URLSource(
        document_id="terms",
        url="https://codeforces.com/terms",
        # O foco é normalizar o HTML para o resultado ser Markdown
        transformers=[
            ContentHTMLTransformer(element="#pageContent"),
            HTML2MarkdownTransformer(
                converter_options={
                    "wrap": True,
                    "wrap_width": 100
                }
            )
        ],
        cache_lifetime=3600, # 1 hora,
        cached_file=data_store.allocate_file("docs", "terms.md"),
        data_store=data_store,

        # Eu particularmente achei algo muito estranho:
        # O site do Codeforces é protegido pelo Cloudflare, e obviamente com os seus desafios
        # de anti-bot, então se você fizer uma requisição simples, ele vai bloquear e retornar
        # um erro 403. Então, para contornar isso, eu adicionei um User-Agent de um navegador
        # e por incrível que pareça, funciona. Apliquei no curl, também. Mas eu que uso
        # PowerShell, algo faz com que o .NET não funciona. Eu não entendo a natureza do Cloudflare.

        # Eu entendo que isso é algo que não é ideal, pois o Cloudflare faz isso para evitar
        # scrapping, por exemplo, mas note que o scrapping que eu faço não tem más intenções.
        request_options={
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0"
            }
        }
    )
)

# Documento 'privacy' - Política de Privacidade do Codeforces
provider.add_source(
    source=URLSource(
        document_id="privacy",
        url="https://codeforces.com/privacy",
        transformers=[
            ContentHTMLTransformer(element="#pageContent"),
            HTML2MarkdownTransformer(
                converter_cls=PrivacyNormalizer,
                converter_options={
                    "wrap": True
                }
            )
        ],
        cache_lifetime=3600, # 1 hora,
        cached_file=data_store.allocate_file("docs", "privacy.md"),
        data_store=data_store,
        request_options={
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0"
            }
        }
    )
)

# Documento 'disclaimer' - Avisos sobre o GPC
provider.add_source(
    source=CacheSource(
        document_id="disclaimer",
        cached_file=data_store.allocate_file(".assets", "docs", "disclaimer.md"),
        cache_lifetime=None,
        data_store=data_store
    )
)

@router.get("/terms", response_class=PlainTextResponse)
def get_terms():
    """Endpoint para obter os Termos e Condições do Codeforces"""
    LOGGER.debug("Recebida requisição em /terms com parâmetros: {}")

    try:
        document = provider.fetch_document("terms")

        return document.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/privacy", response_class=PlainTextResponse)
def get_privacy():
    """Endpoint para obter a Política de Privacidade do Codeforces"""
    LOGGER.debug("Recebida requisição em /privacy com parâmetros: {}")

    try:
        document = provider.fetch_document("privacy")

        return document.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/disclaimer", response_class=PlainTextResponse)
def get_disclaimer():
    """Endpoint para obter os Avisos sobre o GPC"""
    LOGGER.debug("Recebida requisição em /disclaimer com parâmetros: {}")

    try:
        document = provider.fetch_document("disclaimer")

        return document.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
