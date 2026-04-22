Add the patent_sources folder under backend/services/ and update the retrieval MCP server to import and use HybridPatentRetriever.
Recommended retrieval server changes:

from backend.services.patent_sources.hybrid import HybridPatentRetriever
retriever = HybridPatentRetriever()

and in /mcp/command search_patents:
return await retriever.search(query=query, limit=limit)

Ensure config.py defines:
- patent_source
- patent_source_fallback
- lens_api_base_url
- lens_api_token
- patent_request_timeout_seconds
- google_patents_base_url
- google_patents_timeout_seconds
- patent_cache_ttl_seconds
- patent_cache_maxsize
- cpc_seed_patents
- cpc_max_codes
- cpc_second_pass_limit
