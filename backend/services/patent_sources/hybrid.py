from __future__ import annotations

import asyncio

from backend.core.config import settings
from backend.services.patent_sources.base import PatentSearchResult
from backend.services.patent_sources.cpc import select_top_cpcs
from backend.services.patent_sources.lens import LensClient

try:
    from backend.services.patent_sources.google_patents import GooglePatentsSource
except Exception:
    GooglePatentsSource = None


class HybridPatentRetriever:
    def __init__(self) -> None:
        self.lens = LensClient()
        self.google = GooglePatentsSource() if GooglePatentsSource else None

    async def search(self, query: str, limit: int = 10, source_override: str | None = None) -> dict:
        requested_source = (source_override or settings.patent_source or "lens").lower()
        fallback_source = (settings.patent_source_fallback or "none").lower()

        if requested_source == "demo":
            return {
                "source": "demo",
                "strategy": "demo-only",
                "selected_cpc_codes": [],
                "results": [],
            }

        if requested_source == "lens":
            primary = await asyncio.to_thread(self.lens.search, query, limit)
            selected_cpc_codes = select_top_cpcs(primary.get("results", []), max_codes=settings.cpc_max_codes)

            if primary.get("results"):
                return {
                    "source": primary.get("source", "lens"),
                    "strategy": "lens-direct",
                    "selected_cpc_codes": selected_cpc_codes,
                    "results": primary.get("results", []),
                }

            if fallback_source == "google" and self.google:
                try:
                    fallback_results: list[PatentSearchResult] = await asyncio.wait_for(
                        self.google.search(query, limit),
                        timeout=settings.google_patents_timeout_seconds + 2,
                    )
                    return {
                        "source": "google_fallback" if fallback_results else primary.get("source", "lens_empty"),
                        "strategy": "lens-then-google",
                        "selected_cpc_codes": selected_cpc_codes,
                        "results": [item.to_dict() for item in fallback_results],
                    }
                except Exception:
                    pass

            return {
                "source": primary.get("source", "lens_empty"),
                "strategy": "lens-direct",
                "selected_cpc_codes": selected_cpc_codes,
                "results": primary.get("results", []),
            }

        if requested_source == "google" and self.google:
            try:
                primary_results: list[PatentSearchResult] = await asyncio.wait_for(
                    self.google.search(query, limit),
                    timeout=settings.google_patents_timeout_seconds + 2,
                )
                return {
                    "source": "google",
                    "strategy": "google-direct",
                    "selected_cpc_codes": select_top_cpcs([item.to_dict() for item in primary_results], max_codes=settings.cpc_max_codes),
                    "results": [item.to_dict() for item in primary_results],
                }
            except Exception:
                return {"source": "google_error", "strategy": "google-direct", "selected_cpc_codes": [], "results": []}

        return {"source": "unsupported_source", "strategy": "none", "selected_cpc_codes": [], "results": []}