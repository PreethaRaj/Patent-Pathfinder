import pytest

from backend.services.reporting import ReportingService

@pytest.mark.asyncio
async def test_report_service_smoke(monkeypatch):
    class DummyClient:
        async def command(self, command: str, arguments: dict) -> dict:
            return {"artifact_path": "/tmp/demo.csv", "format": "csv"}

    service = ReportingService()
    service.client = DummyClient()
    result = await service.create_report("demo-id", "csv")
    assert result["format"] == "csv"
