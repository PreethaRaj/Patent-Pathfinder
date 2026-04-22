# Production-Hardened Lite Edition

This edition is designed for low-volume production, staging, demos, and developer validation while preserving the MCP-first architecture from the project brief and PRD.

## What changes in lite mode

- Default provider switches to `ollama`
- Default chat model switches to `qwen2.5:7b-instruct`
- Default embedding model switches to `nomic-embed-text`
- Compose adds health checks, restart policies, and service dependency conditions
- Frontend runs in production mode instead of dev mode
- Kubernetes includes smaller resource requests and limits

## Bootstrap

```bash
cp .env.lite.example .env
./scripts/bootstrap-lite.sh
```

## Smoke test

```bash
./scripts/smoke-test-lite.sh
```

## Production notes

- Suitable for internal teams, pilots, and low-throughput deployments
- Keep the same MCP contracts and API surface as the full edition
- Scale backend and MCP replicas before scaling model size
- Use managed backups for Postgres and snapshot policies for OpenSearch/Neo4j
