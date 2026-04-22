#!/usr/bin/env bash
set -euo pipefail

curl -fsS http://localhost:8000/healthz >/dev/null
curl -fsS http://localhost:8101/healthz >/dev/null
curl -fsS http://localhost:8102/healthz >/dev/null
curl -fsS http://localhost:8103/healthz >/dev/null
curl -fsS http://localhost:8104/healthz >/dev/null
curl -fsS http://localhost:8105/healthz >/dev/null
curl -fsS http://localhost:8106/healthz >/dev/null

curl -fsS -X POST http://localhost:8000/api/v1/ideas/analyze \
  -H 'Content-Type: application/json' \
  -d '{"title":"Warehouse Stockout Prediction","problem_statement":"I want an AI system that predicts warehouse stockouts using camera feeds from shelves and ERP inventory signals. The model should alert managers when a shelf is empty before the ERP catches up.","domain":"retail-operations","objectives":["camera-based shelf monitoring","ERP signal integration","pre-ERP stockout alerting"]}' | python -m json.tool >/dev/null

echo "Lite smoke test passed."
