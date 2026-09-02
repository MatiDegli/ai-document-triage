# AI Document Triage

AI Document Triage is a backend service for structured document analysis using
LLM providers.

The API stores documents in PostgreSQL and sends them to a pluggable provider
that returns validated analysis results. The current implementation integrates
DeepSeek for live requests and includes a deterministic mock provider for local
development and testing.

The service is built around provider abstraction, schema-constrained outputs,
persistent analysis records, and reproducible local development. It uses
FastAPI, SQLAlchemy, Alembic, Docker Compose, pytest, Ruff, Pyright, and
GitHub Actions.

## Requirements

- Python 3.14
- [uv](https://docs.astral.sh/uv/)
- Docker Desktop

## Setup

Run these commands from the repository root.

Create the local environment file:

```powershell
Copy-Item .env.example .env
```

Set the test database URL in `.env`:

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

Run the tests:

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

FastAPI provides interactive documentation at:

`http://localhost:8000/docs`

The document endpoints are:

```text
GET  /health
POST /documents
GET  /documents
GET  /documents/{document_id}
```

Example request body:

```json
{
  "title": "Example",
  "content": "Document content"
}
```

## Stop the Services

Stop the containers while keeping the PostgreSQL data:

```powershell
docker compose down
```

Remove the containers and the PostgreSQL volume when a clean database is
needed:

```powershell
docker compose down -v
```

The command reference is in [`docs/commands.md`](docs/commands.md). The SQL
examples are in [`docs/sql-notes.md`](docs/sql-notes.md).
