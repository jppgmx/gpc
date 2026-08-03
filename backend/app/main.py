from fastapi import FastAPI

app = FastAPI(title="GPC Backend")

@app.get("/health")
def health_check():
    return {"status": "ok"}
