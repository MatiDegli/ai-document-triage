from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello world"}


# Registra una ruta GET en /health
@app.get("/health")
def health_check() -> dict[str, str]:
    # Devuelve un JSON simple indicando que la API esta viva
    return {"status": "ok"}
