param(
  [Parameter(Mandatory=$true)][string]$Query,
  [int]$BatchSize = 25,
  [int]$MaxRecords = 100
)

$payload = @{
  command = "ingest_lens_patents"
  arguments = @{
    query = $Query
    batch_size = $BatchSize
    max_records = $MaxRecords
  }
} | ConvertTo-Json -Depth 6

Invoke-RestMethod -Method Post -Uri "http://localhost:8102/mcp/command" -ContentType "application/json" -Body $payload
