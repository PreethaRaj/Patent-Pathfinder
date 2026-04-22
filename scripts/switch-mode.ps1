param(
  [Parameter(Mandatory=$true)]
  [ValidateSet("demo","lens","local")]
  [string]$Mode
)

$envFile = Join-Path $PSScriptRoot "..\.env"
if (-not (Test-Path $envFile)) {
  Write-Error ".env not found. Create it first from .env.lite.example"
  exit 1
}
$content = Get-Content $envFile
$updated = $false
for ($i=0; $i -lt $content.Length; $i++) {
  if ($content[$i] -match '^PATENT_SOURCE=') {
    $content[$i] = "PATENT_SOURCE=$Mode"
    $updated = $true
  }
}
if (-not $updated) { $content += "PATENT_SOURCE=$Mode" }
Set-Content -Path $envFile -Value $content
Write-Host "Set PATENT_SOURCE=$Mode in .env"
Write-Host "Restart the stack to apply: docker compose -f docker-compose.yml -f docker-compose.lite.yml up -d --build"
