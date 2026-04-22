from backend.ingestion.lens_ingest import ingest_lens_patent_by_id, ingest_lens_patents
from backend.mcp_servers.common import create_mcp_app
from backend.services.lens_client import LensClient


async def ingest_documents(args: dict) -> dict:
    query = args.get("query")
    if not query:
        return {"error": "query is required", "ingested": 0}
    batch_size = int(args.get("batch_size", 25))
    max_records = int(args.get("max_records", 100))
    return await ingest_lens_patents(query, batch_size=batch_size, max_records=max_records)


async def ingest_patent_by_id(args: dict) -> dict:
    lens_id = args.get("lens_id")
    if not lens_id:
        return {"error": "lens_id is required"}
    return await ingest_lens_patent_by_id(lens_id)


async def quota_status(args: dict) -> dict:
    del args
    return {"quota": LensClient().quota_snapshot()}


app = create_mcp_app(
    "mcp_ingestion",
    "0.2.0",
    {
        "ingest_documents": ingest_documents,
        "ingest_lens_patents": ingest_documents,
        "ingest_patent_by_id": ingest_patent_by_id,
        "quota_status": quota_status,
    },
)
