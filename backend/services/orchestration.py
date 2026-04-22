from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from backend.core.config import settings
from backend.models.schemas import IdeaCreate
from backend.services.mcp_client import MCPClient


def _derive_features(payload: IdeaCreate) -> list[dict[str, str]]:
    candidates = [
        payload.title.strip(),
        payload.problem_statement.strip(),
        *[o.strip() for o in payload.objectives if o.strip()],
        *[c.strip() for c in payload.constraints if c.strip()],
        *[t.strip() for t in payload.tags if t.strip()],
    ]
    features: list[dict[str, str]] = []
    seen = set()

    for idx, text in enumerate(candidates, start=1):
        if not text:
            continue
        normalized = text.lower()
        if normalized in seen:
            continue
        seen.add(normalized)
        features.append({"id": f"F{idx}", "name": text[:120], "novelty_label": "unknown"})
        if len(features) >= 5:
            break

    if not features:
        features = [{"id": "F1", "name": "Core invention concept", "novelty_label": "unknown"}]
    return features


def _build_novelty_map(feature_to_evidence_mapping: list[dict[str, Any]]) -> dict[str, list[str]]:
    novelty_map = {
        "high_saturation": [],
        "moderate_saturation": [],
        "potential_novelty_hotspots": [],
    }

    for item in feature_to_evidence_mapping:
        feature_id = item.get("feature_id")
        evidence_count = len(item.get("evidence") or [])
        if evidence_count >= 2:
            novelty_map["high_saturation"].append(feature_id)
        elif evidence_count == 1:
            novelty_map["moderate_saturation"].append(feature_id)
        else:
            novelty_map["potential_novelty_hotspots"].append(feature_id)

    return novelty_map


def _build_redesign_suggestions(feature_to_evidence_mapping: list[dict[str, Any]], query: str) -> list[str]:
    low_evidence = [item.get("feature_name") for item in feature_to_evidence_mapping if not (item.get("evidence") or [])]
    if low_evidence:
        anchor = low_evidence[0]
        return [
            f"Emphasize {anchor.lower()} as the likely differentiator.",
            f"Describe implementation constraints for {anchor.lower()} more concretely.",
            "Clarify the decision logic, timing, or system integration details to differentiate further.",
        ]
    return [
        f"Narrow the claim scope around the least saturated part of: {query[:120]}",
        "Add deployment or hardware constraints that are less common in prior art.",
        "Differentiate the feature interaction and control logic more explicitly.",
    ]


class Orchestrator:
    def __init__(self) -> None:
        self.retrieval = MCPClient(settings.mcp_retrieval_url)
        self.evidence = MCPClient(settings.mcp_evidence_url)
        self.novelty = MCPClient(settings.mcp_novelty_url)
        self.report = MCPClient(settings.mcp_report_url)

    async def analyze_idea(self, payload: IdeaCreate, source_override: str | None = None) -> dict[str, Any]:
        requested_source = (source_override or settings.patent_source).lower()

        patent_results = await self.retrieval.command(
            "search_patents",
            {
                "query": payload.problem_statement or payload.title,
                "limit": 10,
                "source": requested_source,
            },
        )

        results = patent_results.get("results", []) or []
        features = _derive_features(payload)

        evidence_payload = await self.evidence.command(
            "map_features_to_passages",
            {"features": features, "comparables": results},
        )
        evidence_mappings = evidence_payload.get("mappings", []) or []

        novelty_payload = await self.novelty.command("score_novelty", {"comparables": results})
        feature_to_evidence_mapping = [
            {
                "feature_id": mapping.get("feature_id") or feature["id"],
                "feature_name": mapping.get("feature_name") or mapping.get("feature") or feature["name"],
                "overlap_label": mapping.get("overlap_label") or "unknown",
                "evidence": mapping.get("evidence") or ([] if not mapping.get("passage") else [mapping.get("passage")]),
            }
            for feature, mapping in zip(features, evidence_mappings or [{} for _ in features], strict=False)
        ]

        novelty_map = _build_novelty_map(feature_to_evidence_mapping)
        redesign_suggestions = _build_redesign_suggestions(feature_to_evidence_mapping, payload.problem_statement or payload.title)

        top_prior_art = []
        evidence_items = []
        for item in results[:5]:
            passage = (item.get("snippets") or [item.get("abstract") or ""])[:1][0]
            publication_number = item.get("publication_number") or item.get("id") or "unknown"
            title = item.get("title") or "Untitled patent result"

            top_prior_art.append(
                {
                    "publication_number": publication_number,
                    "title": title,
                    "evidence": [passage] if passage else [],
                }
            )

            if passage:
                evidence_items.append(
                    {
                        "source_id": publication_number,
                        "source_type": "patent",
                        "title": title,
                        "passage": passage,
                        "score": float(item.get("score", 0.0) or 0.0),
                        "citation": publication_number,
                    }
                )

        suggested_cpc_codes = patent_results.get("selected_cpc_codes") or []
        search_expansions = [payload.problem_statement or payload.title, *suggested_cpc_codes]
        retrieval_source = patent_results.get("source") or requested_source
        analysis_mode = "demo" if requested_source == "demo" else "lens" if requested_source == "lens" else requested_source

        return {
            "idea_id": str(uuid4()),
            "title": payload.title,
            "status": "analyzed",
            "created_at": datetime.now(timezone.utc),
            "analysis_mode": analysis_mode,
            "retrieval_source": retrieval_source,
            "evidence": evidence_items,
            "novelty": {
                "overlap_score": float(novelty_payload.get("overlap_score", 0.0) or 0.0),
                "saturation_level": novelty_payload.get("saturation_level", "unknown"),
                "recommendations": novelty_payload.get("recommendations") or redesign_suggestions,
                "clusters": results,
            },
            "decomposed_features": features,
            "top_prior_art": top_prior_art,
            "feature_to_evidence_mapping": feature_to_evidence_mapping,
            "novelty_map": novelty_map,
            "redesign_suggestions": redesign_suggestions,
            "suggested_cpc_codes": suggested_cpc_codes,
            "suggested_search_expansions": search_expansions,
        }