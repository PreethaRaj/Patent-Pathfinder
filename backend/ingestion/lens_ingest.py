from __future__ import annotations

from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models import PatentChunk, PatentDocument
from backend.db.session import AsyncSessionLocal
from backend.services.lens_client import LensClient, extract_cpc_codes, extract_parties, extract_publication_numbers, extract_text, extract_title


def chunk_text(text: str, size: int = 900, overlap: int = 120) -> list[str]:
    if not text:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + size)
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks


def normalize_patent(record: dict[str, Any]) -> dict[str, Any]:
    cpcs = extract_cpc_codes(record)
    abstract = record.get("abstract")
    abstract_text = abstract[0].get("text") if isinstance(abstract, list) and abstract and isinstance(abstract[0], dict) else None
    return {
        "lens_id": record["lens_id"],
        "jurisdiction": record.get("jurisdiction"),
        "title": extract_title(record),
        "abstract": abstract_text,
        "full_text": extract_text(record),
        "publication_numbers": extract_publication_numbers(record),
        "applicants": extract_parties(record, "applicants"),
        "inventors": extract_parties(record, "inventors"),
        "cpc_classes": cpcs,
        "source_url": f"https://lens.org/{record['lens_id']}",
        "raw_payload": record,
    }


async def upsert_patent(session: AsyncSession, patent: dict[str, Any]) -> PatentDocument:
    existing = await session.scalar(select(PatentDocument).where(PatentDocument.lens_id == patent["lens_id"]))
    if existing is None:
        existing = PatentDocument(**patent)
        session.add(existing)
        await session.flush()
    else:
        for key, value in patent.items():
            setattr(existing, key, value)
        await session.flush()
        await session.execute(delete(PatentChunk).where(PatentChunk.patent_id == existing.id))

    text = ((patent.get("abstract") or "") + "\n\n" + (patent.get("full_text") or "")).strip()
    for idx, chunk in enumerate(chunk_text(text)):
        session.add(PatentChunk(patent_id=existing.id, chunk_index=idx, content=chunk, metadata={"lens_id": patent["lens_id"]}))
    return existing


async def ingest_lens_patents(query: str, *, batch_size: int = 25, max_records: int = 100) -> dict[str, Any]:
    client = LensClient()
    total = 0
    ingested: list[dict[str, Any]] = []
    offset = 0
    async with AsyncSessionLocal() as session:
        while total < max_records:
            response = await client.search_patents(query, size=min(batch_size, max_records - total), offset=offset)
            records = response.get("data") or []
            if not records:
                break
            for record in records:
                normalized = normalize_patent(record)
                doc = await upsert_patent(session, normalized)
                ingested.append(
                    {
                        "lens_id": doc.lens_id,
                        "title": doc.title,
                        "jurisdiction": doc.jurisdiction,
                        "publication_numbers": doc.publication_numbers,
                    }
                )
                total += 1
                if total >= max_records:
                    break
            await session.commit()
            offset += len(records)
            if len(records) < batch_size:
                break
    return {"query": query, "ingested": ingested, "count": len(ingested), "quota": client.quota_snapshot()}


async def ingest_lens_patent_by_id(lens_id: str) -> dict[str, Any]:
    client = LensClient()
    record = await client.get_patent(lens_id)
    normalized = normalize_patent(record)
    async with AsyncSessionLocal() as session:
        doc = await upsert_patent(session, normalized)
        await session.commit()
    return {
        "lens_id": doc.lens_id,
        "title": doc.title,
        "jurisdiction": doc.jurisdiction,
        "publication_numbers": doc.publication_numbers,
        "quota": client.quota_snapshot(),
    }
