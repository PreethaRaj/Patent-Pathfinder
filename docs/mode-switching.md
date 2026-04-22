# Mode switching

The project supports three patent retrieval modes controlled by `PATENT_SOURCE` in `.env`:

- `demo`: seeded prior-art examples, no external API dependency
- `local`: query only locally ingested patents
- `lens`: query the live Lens API

## Windows PowerShell

```powershell
Copy-Item .env.lite.example .env
.\scripts\switch-mode.ps1 -Mode demo
.\scripts\bootstrap-lite.ps1
.\scripts\smoke-test-lite.ps1
```

Switch to Lens later:

```powershell
notepad .env
# set LENS_API_TOKEN=...
.\scripts\switch-mode.ps1 -Mode lens
docker compose -f docker-compose.yml -f docker-compose.lite.yml up -d --build
```
