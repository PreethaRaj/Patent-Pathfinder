from pathlib import Path

from backend.core.config import get_settings


def test_lens_env_defaults_present():
    settings = get_settings()
    assert settings.lens_api_base_url.startswith("https://")
    assert settings.lens_patent_batch_size <= 100
    assert settings.lens_requests_per_minute <= 10


def test_retrieval_server_uses_no_mock_patent_fixture():
    content = Path("backend/mcp_servers/retrieval/server.py").read_text()
    assert "patent-001" not in content
    assert "search_local_patents" in content
