# syntax=docker/dockerfile:1

FROM astral/uv:python3.12-bookworm-slim

WORKDIR /usr/src/app

COPY . .

RUN uv sync 

EXPOSE 8000

CMD ["uv", "run", "fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]