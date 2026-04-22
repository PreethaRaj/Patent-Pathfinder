from backend.mcp_servers.common import create_mcp_app


def _feature_name(feature) -> str:
    if isinstance(feature, dict):
        return str(
            feature.get("name")
            or feature.get("feature_name")
            or feature.get("id")
            or "Unnamed feature"
        )
    return str(feature)


def _feature_id(feature, idx: int) -> str:
    if isinstance(feature, dict):
        return str(feature.get("id") or f"F{idx + 1}")
    return f"F{idx + 1}"


async def map_features_to_passages(args: dict) -> dict:
    features = args.get("features", []) or []
    comparables = args.get("comparables", []) or []

    mappings = []

    # If no comparables → return empty evidence cleanly
    if not comparables:
        for idx, feature in enumerate(features):
            mappings.append(
                {
                    "feature_id": _feature_id(feature, idx),
                    "feature": _feature_name(feature),
                    "feature_name": _feature_name(feature),
                    "passage": None,
                    "score": None,
                    "citation": None,
                    "overlap_label": "no_evidence",
                    "evidence": [],
                }
            )
        return {"mappings": mappings}

    # Proper mapping logic (no fake assignment)
    for idx, feature in enumerate(features):
        fname = _feature_name(feature).lower()

        matched = []

        for comp in comparables:
            abstract = comp.get("abstract") or ""
            snippets = comp.get("snippets") or []
            text = " ".join(snippets) if snippets else abstract

            if not text:
                continue

            # simple relevance check
            if fname in text.lower():
                matched.append(comp)

        # If nothing matches → leave empty
        if not matched:
            mappings.append(
                {
                    "feature_id": _feature_id(feature, idx),
                    "feature": _feature_name(feature),
                    "feature_name": _feature_name(feature),
                    "passage": None,
                    "score": None,
                    "citation": None,
                    "overlap_label": "no_evidence",
                    "evidence": [],
                }
            )
            continue

        # Use best match (first for now)
        best = matched[0]

        abstract = best.get("abstract") or ""
        snippets = best.get("snippets") or []

        passage = snippets[0] if snippets else abstract

        citation = (
            best.get("id")
            or best.get("publication_number")
            or best.get("lens_id")
        )

        mappings.append(
            {
                "feature_id": _feature_id(feature, idx),
                "feature": _feature_name(feature),
                "feature_name": _feature_name(feature),
                "passage": passage,
                "score": best.get("score"),
                "citation": citation,
                "overlap_label": "covered",
                "evidence": [passage] if passage else [],
            }
        )

    return {"mappings": mappings}


app = create_mcp_app(
    "mcp_evidence",
    "1.0.0",
    {"map_features_to_passages": map_features_to_passages},
)