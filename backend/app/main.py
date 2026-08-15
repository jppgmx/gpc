"""
    Entrypoint do servidor
"""

from asyncio import create_task
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import docs, calendar, problemset, contests
from services.data_store import DataStore
from services.logging import setup_logging
from services.worker import start_worker

@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Gerencia o ciclo de vida do servidor """
    
    # Configura o logging
    store = DataStore()
    setup_logging(store)

    # Inicia o worker em segundo plano
    task = create_task(start_worker())
    yield
    task.cancel()

app = FastAPI(
    title="GPC Backend",
    description="Backend para o sistema GPC",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan
)
app.include_router(docs.router, prefix="/docs")
app.include_router(calendar.router, prefix="/api")
app.include_router(problemset.router, prefix="/api")
app.include_router(contests.router, prefix="/api")

@app.get("/health")
def health_check():
    """Endpoint de verificação de saúde do servidor"""
    return {"status": "ok"}
