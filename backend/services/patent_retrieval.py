from __future__ import annotations

import json
from pathlib import Path

from backend.core.config import settings


async def search_demo_patents(query: str, limit: int = 10) -> list[dict]:
    """Load and score seeded demo prior art from sample data."""
    path = Path(settings.demo_data_path)
    if not path.exists():
        return []

    data = json.loads(path.read_text(encoding="utf-8"))

    # Support either a plain list of patent-like dicts or the warehouse demo structure.
    if isinstance(data, list):
        raw_results = data
    else:
        raw_results = data.get("results", [])
        if not raw_results and data.get("top_prior_art"):
            raw_results = [
                {
                    "id": item.get("publication_number", f"demo-{idx+1}"),
                    "title": item.get("title", "Untitled patent"),
                    "abstract": " ".join(item.get("evidence", [])),
                    "snippets": item.get("evidence", []),
                    "score": 0.5,
                    "source": "demo",
                }
                for idx, item in enumerate(data.get("top_prior_art", []))
            ]

    q_words = [w for w in query.lower().split() if w]
    scored: list[dict] = []
    for item in raw_results:
        title = item.get("title", "")
        abstract = item.get("abstract", "")
        snippets = item.get("snippets", []) or []
        haystack = f"{title} {abstract} {' '.join(snippets)}".lower()
        score = sum(1 for word in q_words if word in haystack) / max(len(q_words), 1)
        scored.append({
            **item,
            "id": item.get("id") or item.get("publication_number") or "demo-unknown",
            "title": title or "Untitled patent",
            "abstract": abstract,
            "snippets": snippets if snippets else ([abstract[:300]] if abstract else []),
            "score": round(max(score, float(item.get("score", 0.0))), 3),
            "source": item.get("source", "demo"),
        })

    scored.sort(key=lambda x: x.get("score", 0.0), reverse=True)
    return scored[:limit]


async def search_local_patents(query: str, limit: int = 10) -> list[dict]:
    """Search locally indexed patents via OpenSearch. Returns empty on any failure."""
    try:
        from opensearchpy import AsyncOpenSearch

        client = AsyncOpenSearch(hosts=[settings.opensearch_url])
        resp = await client.search(
            index=settings.opensearch_index,
            body={
                "query": {"multi_match": {"query": query, "fields": ["title^2", "abstract", "content"]}},
                "size": limit,
            },
        )
        hits = resp.get("hits", {}).get("hits", [])
        return [
            {
                "id": h.get("_id"),
                "score": h.get("_score", 0.0),
                **h.get("_source", {}),
            }
            for h in hits
        ]
    except Exception:
        return []
