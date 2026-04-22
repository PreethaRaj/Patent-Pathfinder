from backend.core.config import settings
from backend.mcp_servers.common import create_mcp_app
from backend.services.patent_retrieval import search_demo_patents
from backend.services.patent_sources.hybrid import HybridPatentRetriever

retriever = HybridPatentRetriever()


async def search_patents(args: dict) -> dict:
    query = str(args.get("query", "")).strip()
    limit = int(args.get("limit", 10))
    requested_source = str(args.get("source") or settings.patent_source).lower()

    if requested_source == "demo":
        results = await search_demo_patents(query, limit=limit)
        return {
            "results": results,
            "source": "demo",
            "strategy": "demo-seeded",
            "selected_cpc_codes": [],
        }

    return await retriever.search(query=query, limit=limit, source_override=requested_source)


async def search_papers(args: dict) -> dict:
    del args
    return {"results": [], "source": "not-configured"}


app = create_mcp_app(
    "mcp_retrieval",
    "1.0.0",
    {
        "search_patents": search_patents,
        "search_papers": search_papers,
        "hybrid_search": search_patents,
    },
)