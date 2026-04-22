FROM python:3.12-slim AS backend-builder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && rm -rf /var/lib/apt/lists/*
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --upgrade pip && pip install --prefix=/install -r /app/backend/requirements.txt
COPY backend /app/backend
COPY docs /app/docs
RUN python -m compileall /app/backend

FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/usr/local/bin:$PATH"
WORKDIR /app
COPY --from=backend-builder /install /usr/local
COPY --from=backend-builder /app/backend /app/backend
COPY --from=backend-builder /app/docs /app/docs
EXPOSE 8000
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
