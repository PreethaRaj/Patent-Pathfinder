import json
from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.main import app


def test_warehouse_stockout_fixture_is_consistent():
    fixture = json.loads(Path("backend/tests/fixtures/warehouse_stockout_expected.json").read_text())
    assert fixture["idea_title"] == "Warehouse Stockout Prediction"
    assert len(fixture["decomposed_features"]) == 4
    assert fixture["novelty_map"]["potential_hotspots"] == ["F4"]
    assert any("temporal lag" in item.lower() for item in fixture["redesign_suggestions"])


def test_warehouse_stockout_api_contract(monkeypatch):
    async def fake_analyze(self, payload):
        return {
            "idea_id": "demo-warehouse-stockout",
            "title": payload.title,
            "status": "analyzed",
            "created_at": "2026-04-17T00:00:00Z",
            "evidence": [
                {
                    "source_id": "US11514409B2",
                    "source_type": "patent",
                    "title": "Camera-based shelf monitoring",
                    "passage": "Shelf monitoring with computer vision for detecting empty shelves.",
                    "score": 0.92,
                    "citation": "claims 1-5",
                },
                {
                    "source_id": "EP3982345A1",
                    "source_type": "patent",
                    "title": "ERP inventory signal integration",
                    "passage": "Inventory prediction using ERP and sensors.",
                    "score": 0.88,
                    "citation": "paragraphs 45-67",
                },
            ],
            "novelty": {
                "overlap_score": 0.81,
                "saturation_level": "high for F1-F3, lower for F4",
                "recommendations": [
                    "Focus on camera + ERP temporal lag prediction.",
                    "Add explicit edge-device deployment constraints.",
                    "Explore multi-modal fusion with audio or weight sensors.",
                ],
                "clusters": [
                    {"id": "US11514409B2", "title": "Shelf monitoring with computer vision", "score": 0.92},
                    {"id": "EP3982345A1", "title": "Inventory prediction using ERP and sensors", "score": 0.88},
                ],
            },
        }

    monkeypatch.setattr("backend.services.orchestration.Orchestrator.analyze_idea", fake_analyze)
    client = TestClient(app)
    response = client.post(
        "/api/v1/ideas",
        json={
            "title": "Warehouse Stockout Prediction",
            "problem_statement": "I want an AI system that predicts warehouse stockouts using camera feeds from shelves and ERP inventory signals. The model should alert managers when a shelf is empty before the ERP catches up.",
            "domain": "retail-operations",
            "objectives": [
                "Camera-based shelf monitoring",
                "ERP inventory signal integration",
                "Stockout prediction model",
                "Pre-ERP alerting based on temporal lag",
            ],
            "constraints": ["Local models only", "MCP-first tool calling"],
            "tags": ["warehouse", "computer-vision", "erp", "stockout"],
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["title"] == "Warehouse Stockout Prediction"
    assert len(payload["evidence"]) == 2
    assert payload["novelty"]["recommendations"][0].startswith("Focus on camera + ERP temporal lag")
