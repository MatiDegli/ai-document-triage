from fastapi import FastAPI

from app.api.documents import router as documents_router


app = FastAPI()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello world"}


# Registra una ruta GET en /health
@app.get("/health")
def health_check() -> dict[str, str]:
    # Devuelve un JSON simple indicando que la API esta viva
    return {"status": "ok"}


app.include_router(documents_router)
