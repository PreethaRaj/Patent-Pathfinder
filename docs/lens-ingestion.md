# Lens patent ingestion

This edition uses the live Lens Patent API for patent ingestion. Add `LENS_API_TOKEN` to `.env`, then call the MCP ingestion server or the helper script to ingest patent data into PostgreSQL.

## MCP commands
- `ingest_lens_patents` with `{query, batch_size, max_records}`
- `ingest_patent_by_id` with `{lens_id}`
- `quota_status`


## Retrieval strategy

The retrieval path now uses a two-pass workflow:

1. Run a keyword search to find the most relevant seed patents.
2. Inspect CPC codes on the top seed patents.
3. Re-run retrieval with the original query plus the strongest CPC codes.
4. Merge and rerank results so patents using different wording but the same technical classification are surfaced.
