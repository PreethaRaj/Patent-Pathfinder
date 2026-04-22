from fastapi.testclient import TestClient

from backend.mcp_servers.retrieval.server import app as retrieval_app


def test_retrieval_server_search():
    client = TestClient(retrieval_app)
    response = client.post("/mcp/command", json={"command": "search_patents", "arguments": {"query": "packaging"}})
    assert response.status_code == 200
    payload = response.json()
    assert payload["strategy"] == "keyword-first-then-cpc"
    assert isinstance(payload["selected_cpc_codes"], list)
    assert payload["results"][0]["source_type"] == "patent"
