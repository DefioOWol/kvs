FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock /app
COPY protos /app/protos
COPY server /app/server

RUN pip install --no-cache-dir --upgrade uv && uv sync --frozen --no-dev

CMD ["python", "server/main.py"]
