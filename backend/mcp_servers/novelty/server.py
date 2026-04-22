from backend.mcp_servers.common import create_mcp_app


async def score_novelty(args: dict) -> dict:
    overlaps = args.get("comparables", [])
    avg_score = sum(float(item.get("score", 0.0)) for item in overlaps) / max(len(overlaps), 1)
    overlap_score = round(avg_score, 3)
    novelty_score = round(max(0.0, 1.0 - avg_score), 3)
    saturation = "low" if overlap_score < 0.35 else "medium" if overlap_score < 0.65 else "high"
    recommendations = [
        "Emphasize constraints and integrations not present in the top retrieved patents.",
        "Inspect the highest-scoring cited passages before drafting claims.",
    ]
    return {
        "overlap_score": overlap_score,
        "novelty_score": novelty_score,
        "saturation_level": saturation,
        "recommendations": recommendations,
    }


async def saturation_analysis(args: dict) -> dict:
    overlaps = args.get("comparables", [])
    avg_score = sum(float(item.get("score", 0.0)) for item in overlaps) / max(len(overlaps), 1)
    return {"market": args.get("market", "general"), "saturation_index": round(avg_score, 3)}


app = create_mcp_app(
    "mcp_novelty",
    "0.2.0",
    {
        "score_novelty": score_novelty,
        "saturation_analysis": saturation_analysis,
    },
)
