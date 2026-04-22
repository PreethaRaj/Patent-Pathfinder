from fastapi import FastAPI
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.responses import Response

REQUEST_COUNT = Counter("innovation_requests_total", "Total API requests", ["route", "method"])
REQUEST_LATENCY = Histogram("innovation_request_latency_seconds", "Latency", ["route", "method"])

metrics_app = FastAPI()

@metrics_app.get("/")
async def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
