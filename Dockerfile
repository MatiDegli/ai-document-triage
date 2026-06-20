# syntax=docker/dockerfile:1

FROM astral/uv:python3.12-bookworm-slim
RUN uv init test
RUN cd test && uv add fastapi[standard]
RUN cd test && fastapi dev