# API Specification

## POST /api/v1/ideas
Creates and analyzes an idea.

### Example request

```json
{
  "title": "Warehouse Stockout Prediction",
  "problem_statement": "I want an AI system that predicts warehouse stockouts using camera feeds from shelves and ERP inventory signals. The model should alert managers when a shelf is empty before the ERP catches up.",
  "domain": "retail-operations",
  "objectives": [
    "Camera-based shelf monitoring",
    "ERP inventory signal integration",
    "Stockout prediction model",
    "Pre-ERP alerting based on temporal lag"
  ],
  "constraints": [
    "Local models only",
    "MCP-first tool calling"
  ],
  "tags": ["warehouse", "computer-vision", "erp", "stockout"]
}
```

### Example response shape

```json
{
  "idea_id": "demo-warehouse-stockout",
  "title": "Warehouse Stockout Prediction",
  "status": "analyzed",
  "created_at": "2026-04-17T00:00:00Z",
  "evidence": [
    {
      "source_id": "US11514409B2",
      "source_type": "patent",
      "title": "Camera-based shelf monitoring",
      "passage": "Shelf monitoring with computer vision for detecting inventory conditions.",
      "score": 0.92,
      "citation": "claims 1-5"
    }
  ],
  "novelty": {
    "overlap_score": 0.81,
    "saturation_level": "high for F1-F3, lower for F4",
    "recommendations": [
      "Focus on camera + ERP temporal lag prediction.",
      "Add explicit edge-device deployment constraints.",
      "Explore multi-modal fusion with audio or weight sensors."
    ],
    "clusters": [
      {"id": "US11514409B2", "title": "Shelf monitoring with computer vision", "score": 0.92},
      {"id": "EP3982345A1", "title": "Inventory prediction using ERP and sensors", "score": 0.88}
    ]
  }
}
```

## GET /api/v1/projects
Lists known projects.

## POST /api/v1/reports
Generates a PDF or CSV report.

## GET /healthz
Liveness probe.

## GET /readyz
Readiness probe.
