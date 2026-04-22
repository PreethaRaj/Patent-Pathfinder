# Architecture

## Layers

1. **Frontend**: Next.js App Router UI for idea capture, evidence review, novelty map, and report export.
2. **Backend API**: FastAPI control plane exposing business endpoints.
3. **Orchestrator**: LangGraph workflow coordinating retrieval, grounding, novelty scoring, and reporting.
4. **MCP servers**: Dedicated tool execution services with explicit MCP command schemas.
5. **Infrastructure**: PostgreSQL, OpenSearch, Neo4j, Redis, Celery, Prometheus, Grafana, OTLP.

## Deployment model

- local dev: Docker Compose
- staging/prod: Kubernetes or Helm
- infra bootstrap: Terraform
- GPU workloads: node selectors and resource requests

## Security

- JWT bearer auth
- secret injection via Kubernetes Secret or external secret manager
- network segmentation between API and data services
- local-only LLM endpoints

## Scaling strategy

- API and MCP servers scale horizontally
- Celery workers scale independently
- vLLM scheduled on GPU nodes
- OpenSearch and PostgreSQL use persistent volumes
