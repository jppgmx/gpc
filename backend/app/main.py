from fastapi import FastAPI
from api import docs

app = FastAPI(
    title="GPC Backend",
    description="Backend para o sistema GPC",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)
app.include_router(docs.router, prefix="/docs")

@app.get("/health")
def health_check():
    return {"status": "ok"}
