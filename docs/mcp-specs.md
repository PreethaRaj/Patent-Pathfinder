# MCP Specifications

Each MCP server exposes:

- `GET /mcp` - metadata and command list
- `POST /mcp/command` - execute command
- `GET /healthz` - liveness

## mcp_retrieval

### search_patents
```json
{
  "command": "search_patents",
  "arguments": {
    "query": "compostable barrier coating"
  }
}
```

### search_papers
```json
{
  "command": "search_papers",
  "arguments": {
    "query": "novel oxygen barrier polymer"
  }
}
```

## mcp_ingestion

### ingest_documents
```json
{
  "command": "ingest_documents",
  "arguments": {
    "index": "innovation-documents",
    "documents": [
      {"id": "doc-1", "content": "full text", "metadata": {"source": "pdf"}}
    ]
  }
}
```

## mcp_evidence

### map_features_to_passages
```json
{
  "command": "map_features_to_passages",
  "arguments": {
    "features": ["low oxygen permeability", "biodegradable substrate"]
  }
}
```

## mcp_novelty

### score_novelty
```json
{
  "command": "score_novelty",
  "arguments": {
    "comparables": [{"id": "patent-1"}, {"id": "paper-2"}]
  }
}
```

## mcp_monitoring

### generate_alerts
```json
{
  "command": "generate_alerts",
  "arguments": {
    "topic": "cell-free protein synthesis"
  }
}
```

## mcp_report

### export_report
```json
{
  "command": "export_report",
  "arguments": {
    "report_name": "idea-123",
    "format": "pdf"
  }
}
```
