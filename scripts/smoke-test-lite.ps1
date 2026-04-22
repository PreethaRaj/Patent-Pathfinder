$ErrorActionPreference = "Stop"

function Test-Health($url) {
    $resp = Invoke-WebRequest -UseBasicParsing -Uri $url -TimeoutSec 10
    if ($resp.StatusCode -lt 200 -or $resp.StatusCode -ge 300) {
        throw "Health check failed for $url"
    }
}

Test-Health "http://localhost:8000/healthz"
Test-Health "http://localhost:8101/healthz"
Test-Health "http://localhost:8102/healthz"
Test-Health "http://localhost:8103/healthz"
Test-Health "http://localhost:8104/healthz"
Test-Health "http://localhost:8105/healthz"
Test-Health "http://localhost:8106/healthz"

$payload = @{
    title = "Warehouse Stockout Prediction"
    problem_statement = "I want an AI system that predicts warehouse stockouts using camera feeds from shelves and ERP inventory signals. The model should alert managers when a shelf is empty before the ERP catches up."
    domain = "retail-operations"
    objectives = @(
        "camera-based shelf monitoring",
        "ERP signal integration",
        "pre-ERP stockout alerting"
    )
} | ConvertTo-Json -Depth 5

$response = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/v1/ideas/analyze" -ContentType "application/json" -Body $payload

if (-not $response) {
    throw "Analyze endpoint returned no response."
}

Write-Host "Lite smoke test passed."

Write-Host "Smoke test note: responses include analysis_mode and retrieval_source when available."
