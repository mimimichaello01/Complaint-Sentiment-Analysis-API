FROM python:3.12-slim

WORKDIR /app/src

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --only main --no-root

RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

COPY src/ .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app/src

CMD ["uvicorn", "main:create_app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
