$ErrorActionPreference = "Stop"

if (-not (Test-Path ".env")) {
    Copy-Item ".env.lite.example" ".env"
}

Write-Host "Starting lite services..."
docker compose -f docker-compose.yml -f docker-compose.lite.yml up -d --build postgres redis opensearch neo4j ollama backend frontend celery-worker mcp_retrieval mcp_ingestion mcp_evidence mcp_novelty mcp_monitoring mcp_report prometheus grafana

Write-Host "Waiting for Ollama..."
$maxAttempts = 60
$attempt = 0
do {
    $attempt++
    try {
        $resp = Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:11434/api/tags" -TimeoutSec 5
        if ($resp.StatusCode -eq 200) { break }
    } catch {
        Start-Sleep -Seconds 3
    }
} while ($attempt -lt $maxAttempts)

if ($attempt -ge $maxAttempts) {
    throw "Ollama did not become ready in time."
}

Write-Host "Pulling lite models..."
docker compose exec -T ollama ollama pull qwen2.5:7b-instruct
docker compose exec -T ollama ollama pull nomic-embed-text

Write-Host "Applying migrations..."
docker compose exec -T backend alembic -c backend/db/alembic.ini upgrade head

Write-Host "Loading sample data..."
docker compose exec -T backend python -m backend.ingestion.load_sample_data

Write-Host "Lite environment is ready. Frontend: http://localhost:3000 Backend: http://localhost:8000/docs"

Write-Host "Active patent source:" (Select-String -Path .env -Pattern "^PATENT_SOURCE=" | ForEach-Object { $_.Line })
