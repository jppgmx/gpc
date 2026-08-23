"""
    Entrypoint do servidor
"""

from asyncio import create_task
from contextlib import asynccontextmanager
import psutil

from fastapi import FastAPI

from api import docs, calendar, problemset, contests, tags
from services.data_store import DataStore
from services.logging import setup_logging
from services.profiling import start_profiling
from services.worker import start_worker

@asynccontextmanager
async def lifespan(_: FastAPI):
    """ Gerencia o ciclo de vida do servidor """

    # Configura o logging
    store = DataStore()
    setup_logging(store)

    # Incia o profiling
    profiling = create_task(start_profiling(store))

    # Inicia o worker em segundo plano
    worker = create_task(start_worker())

    yield
    profiling.cancel()
    worker.cancel()

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
app.include_router(tags.router, prefix="/api")
app.include_router(contests.router, prefix="/api")

@app.get("/health")
def health_check():
    """ Endpoint para checagem de saúde do servidor """

    return {
        "status": "ok",
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory": {
            "used_mb": round(psutil.virtual_memory().used / (1024 * 1024), 1),
            "total_mb": round(psutil.virtual_memory().total / (1024 * 1024), 1),
            "percent": psutil.virtual_memory().percent,
        },
    }
