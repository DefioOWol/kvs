FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock /app
COPY protos /app/protos
COPY app /app/app

RUN pip install --no-cache-dir --upgrade uv && uv sync --frozen --no-dev

CMD ["uv", "run", "--no-sync", "python", "-m", "app.main"]
