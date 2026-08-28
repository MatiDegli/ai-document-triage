# Command Reference

Comandos principales para trabajar con `ai-document-triage` durante Week 2.

## Preparar el entorno

Ejecutar desde la raíz del repositorio:

```powershell
uv sync --locked
git status
```

`uv run` ejecuta las herramientas dentro del entorno administrado por uv, por
lo que no es necesario activar `.venv` manualmente.

## Docker Compose

Validar la configuración:

```powershell
docker compose config
```

Levantar solamente PostgreSQL:

```powershell
docker compose up -d postgres
```

Levantar backend y PostgreSQL, reconstruyendo la imagen del backend:

```powershell
docker compose up --build -d
```

Ver servicios activos:

```powershell
docker compose ps
```

Ver logs recientes:

```powershell
docker compose logs postgres --tail 30
docker compose logs backend --tail 30
```

Detener servicios sin eliminar datos:

```powershell
docker compose down
```

Eliminar servicios y también el volumen de PostgreSQL:

```powershell
docker compose down -v
```

Usar `down -v` solamente cuando se quiera reiniciar la base desde cero.

## Alembic

Ver la migración aplicada actualmente:

```powershell
uv run alembic current
```

Ver el historial de migraciones:

```powershell
uv run alembic history
```

Generar una migración a partir de los cambios en los modelos:

```powershell
uv run alembic revision --autogenerate -m "describe the schema change"
```

Revisar el archivo generado antes de aplicarlo.

Aplicar todas las migraciones pendientes:

```powershell
uv run alembic upgrade head
```

Retroceder una migración:

```powershell
uv run alembic downgrade -1
```

`revision --autogenerate` crea un archivo. `upgrade head` modifica la base de
datos. Son operaciones diferentes.

## PostgreSQL

Conectarse a la base `app` expuesta por Compose:

```powershell
psql -U app -h localhost -p 5433 -d app
```

Comandos útiles dentro de `psql`:

```sql
\dt
\d documents
SELECT * FROM documents;
SELECT COUNT(*) FROM documents;
\q
```

El puerto `5433` es el puerto del host. PostgreSQL escucha en el puerto `5432`
dentro del contenedor.

## API

Probar endpoints desde PowerShell:

```powershell
irm http://localhost:8000/
irm http://localhost:8000/health
irm http://localhost:8000/documents
irm http://localhost:8000/docs
```

Crear un documento:

```powershell
irm http://localhost:8000/documents `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"title":"Example","content":"Hello from Postgres"}'
```

Obtener un documento:

```powershell
irm http://localhost:8000/documents/1
```

## Tests y calidad

```powershell
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run pyright
```

Los tests requieren una base de prueba configurada mediante
`TEST_DATABASE_URL`. Esa base debe tener las migraciones aplicadas antes de
ejecutar `pytest`.

## GitHub Actions

Ver ejecuciones recientes con GitHub CLI, si está instalado:

```powershell
gh run list
gh run view --log-failed
```

También se pueden consultar desde la pestaña **Actions** del repositorio en
GitHub.

## Flujo habitual

```text
docker compose up -d postgres
uv run alembic upgrade head
docker compose up --build -d backend
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run pyright
```

