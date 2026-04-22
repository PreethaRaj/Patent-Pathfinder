from __future__ import annotations

import asyncio
import os
from typing import Any

import requests

from backend.services.patent_sources.base import PatentSearchResult


def _first_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts: list[str] = []
        for item in value:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text") or item.get("value") or item.get("abstract") or ""
                if text:
                    parts.append(str(text))
        return " ".join(p for p in parts if p).strip()
    if isinstance(value, dict):
        return str(value.get("text") or value.get("value") or "")
    return ""


def _title_from_patent(p: dict) -> str:
    biblio = p.get("biblio", {}) or {}
    title = biblio.get("invention_title")
    if isinstance(title, list):
        for item in title:
            if isinstance(item, dict) and item.get("text"):
                return str(item["text"])
            if isinstance(item, str):
                return item
    if isinstance(title, dict):
        return str(title.get("text") or "")
    return str(title or p.get("title") or "")


def _publication_number_from_patent(p: dict) -> str:
    biblio = p.get("biblio", {}) or {}
    pub_ref = biblio.get("publication_reference", {}) or {}
    if isinstance(pub_ref, dict):
        jurisdiction = pub_ref.get("jurisdiction") or ""
        doc_number = pub_ref.get("doc_number") or ""
        kind = pub_ref.get("kind") or ""
        combined = f"{jurisdiction}{doc_number}{kind}".strip()
        if combined:
            return combined
    return str(p.get("doc_key") or p.get("lens_id") or "")


def _cpc_codes_from_patent(p: dict) -> list[str]:
    biblio = p.get("biblio", {}) or {}
    raw = biblio.get("classifications_cpc") or p.get("classifications_cpc") or []
    codes: list[str] = []

    if isinstance(raw, list):
        for entry in raw:
            if isinstance(entry, dict):
                if entry.get("symbol"):
                    codes.append(str(entry["symbol"]))
                for cls in entry.get("classifications", []) or []:
                    if isinstance(cls, dict) and cls.get("symbol"):
                        codes.append(str(cls["symbol"]))

    # dedupe preserve order
    seen = set()
    out: list[str] = []
    for code in codes:
        code = code.strip()
        if code and code not in seen:
            seen.add(code)
            out.append(code)
    return out


def _claims_snippets_from_patent(p: dict) -> list[str]:
    claims = p.get("claims") or []
    snippets: list[str] = []
    if isinstance(claims, list):
        for claim in claims[:2]:
            text = _first_text(claim)
            if text:
                snippets.append(text[:400])
    return snippets


class LensClient:
    def __init__(self) -> None:
        self.url = os.getenv("LENS_API_URL", "https://api.lens.org/patent/search")
        self.token = os.getenv("LENS_API_TOKEN")
        self.timeout = int(os.getenv("PATENT_REQUEST_TIMEOUT_SECONDS", "15"))

    def _request(self, payload: dict) -> dict:
        if not self.token:
            return {"source": "lens_unconfigured", "results": []}

        try:
            response = requests.post(
                self.url,
                json=payload,
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                },
                timeout=self.timeout,
            )
            if response.status_code != 200:
                print("Lens status:", response.status_code, response.text[:500])
                return {"source": "lens_error", "results": []}

            body = response.json()
            patents = body.get("data", []) or []

            results: list[dict] = []
            for p in patents:
                abstract = _first_text(p.get("abstract"))
                title = _title_from_patent(p)
                pub_no = _publication_number_from_patent(p)
                cpc_codes = _cpc_codes_from_patent(p)
                snippets = _claims_snippets_from_patent(p)
                if not snippets and abstract:
                    snippets = [abstract[:400]]

                results.append(
                    {
                        "id": str(p.get("lens_id") or pub_no or ""),
                        "publication_number": pub_no or str(p.get("lens_id") or ""),
                        "title": title or "Untitled patent result",
                        "abstract": abstract,
                        "snippets": snippets,
                        "score": 1.0,
                        "source": "lens",
                        "cpc_codes": cpc_codes,
                    }
                )

            if not results:
                return {"source": "lens_empty", "results": []}

            return {"source": "lens", "results": results}

        except Exception as e:
            print("Lens error:", str(e))
            return {"source": "lens_error", "results": []}

    def search(self, query: str, limit: int = 10) -> dict:
        # Stronger than raw plain text, but still no hardcoded content
        payload = {
            "query": {
                "bool": {
                    "should": [
                        {"match": {"title": query}},
                        {"match": {"abstract": query}},
                        {"query_string": {"query": query}},
                    ],
                    "minimum_should_match": 1,
                }
            },
            "size": limit,
        }
        return self._request(payload)

    def search_by_cpc(self, query: str, cpc_codes: list[str], limit: int = 10) -> list[PatentSearchResult]:
        if not cpc_codes:
            return []

        payload = {
            "query": {
                "bool": {
                    "must": [{"query_string": {"query": query}}],
                    "filter": [{"terms": {"classifications_cpc.symbol": cpc_codes}}],
                }
            },
            "size": limit,
        }

        response = self._request(payload)
        items = response.get("results", []) or []
        return [
            PatentSearchResult(
                id=item["id"],
                publication_number=item.get("publication_number", item["id"]),
                title=item.get("title", ""),
                abstract=item.get("abstract", ""),
                snippets=item.get("snippets", []),
                score=float(item.get("score", 0.0) or 0.0),
                source=item.get("source", "lens"),
                cpc_codes=item.get("cpc_codes", []),
            )
            for item in items
        ]