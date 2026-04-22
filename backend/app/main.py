from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
except Exception:  # pragma: no cover
    FastAPIInstrumentor = None

from backend.api.routers import ideas, projects, reports
from backend.core.config import get_settings
from backend.core.metrics import metrics_app
from backend.core.observability import setup_observability

settings = get_settings()
setup_observability(settings)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="Intelligent Innovation Copilot", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True,
)
if FastAPIInstrumentor is not None:
    FastAPIInstrumentor.instrument_app(app)
app.include_router(ideas.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")
app.mount("/metrics", metrics_app)

@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok", "edition": settings.app_edition, "environment": settings.environment, "provider": settings.llm_provider}

@app.get("/readyz")
async def readyz() -> dict[str, str]:
    return {"status": "ready", "edition": settings.app_edition}
