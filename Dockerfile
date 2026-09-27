FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY backend/requirements.txt /app/backend/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/backend/requirements.txt

COPY backend /app/backend

EXPOSE 8080

CMD ["sh", "-c", "python -m google.adk.cli api_server --host 0.0.0.0 --port ${PORT:-8080} --no-reload --allow_origins 'regex:^http://localhost:(5173|8081)$' --no_use_local_storage /app/backend/app/agents"]
