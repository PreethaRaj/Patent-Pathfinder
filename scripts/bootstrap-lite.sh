#!/usr/bin/env bash
set -euo pipefail

cp .env.lite.example .env

docker compose -f docker-compose.yml -f docker-compose.lite.yml up -d --build postgres redis opensearch neo4j ollama backend frontend celery-worker mcp_retrieval mcp_ingestion mcp_evidence mcp_novelty mcp_monitoring mcp_report prometheus grafana

echo "Waiting for Ollama..."
until curl -fsS http://localhost:11434/api/tags >/dev/null; do sleep 3; done

echo "Pulling lite models..."
docker compose exec ollama ollama pull qwen2.5:7b-instruct
docker compose exec ollama ollama pull nomic-embed-text

echo "Applying migrations..."
docker compose exec backend alembic -c backend/db/alembic.ini upgrade head

echo "Loading sample data..."
docker compose exec backend python -m backend.ingestion.load_sample_data

echo "Lite environment is ready. Frontend: http://localhost:3000 Backend: http://localhost:8000/docs"
