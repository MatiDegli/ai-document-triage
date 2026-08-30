# AI Document Triage

A small didactic project for learning backend and DevOps technologies.
The application provides a FastAPI API for creating and retrieving documents
persisted in PostgreSQL.

## Requirements

- Python 3.14
- [uv](https://docs.astral.sh/uv/)
- Docker Desktop

## Setup

Create the local environment file:

```powershell
Copy-Item .env.example .env
```

Add the test database URL to `.env`:

```env
TEST_DATABASE_URL=postgresql+psycopg://app:app@localhost:5433/app_test
```

Install the project dependencies:

```powershell
uv sync --locked
```

## Run the Application

Start the backend and PostgreSQL services:

```powershell
docker compose up --build -d
```

Apply the database migrations:

```powershell
uv run alembic upgrade head
```

The API is available at `http://localhost:8000`.

## Run Tests

Create the test database once:

```powershell
docker compose exec -T postgres createdb -U app app_test
```

Apply the migrations to the test database:

```powershell
$env:DATABASE_URL = "postgresql+psycopg://app:app@localhost:5433/app_test"
uv run alembic upgrade head
Remove-Item Env:DATABASE_URL
```

Run the test suite:

```powershell
uv run pytest
```

## Quality Checks

```powershell
uv run ruff check .
uv run ruff format --check .
uv run pyright
```

## API

Interactive documentation: `http://localhost:8000/docs`

Available endpoints:

```text
GET  /health
POST /documents
GET  /documents
GET  /documents/{document_id}
```

Example document payload:

```json
{
  "title": "Example",
  "content": "Document content"
}
```

## Stop the Services

```powershell
docker compose down
```

The PostgreSQL data is preserved in the named Docker volume. To remove the
volume as well, use `docker compose down -v`.

More command examples are available in [`docs/commands.md`](docs/commands.md),
and SQL examples are available in [`docs/sql-notes.md`](docs/sql-notes.md).
