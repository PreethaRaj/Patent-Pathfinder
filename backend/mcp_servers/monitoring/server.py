from datetime import datetime, timezone

from backend.mcp_servers.common import create_mcp_app

async def generate_alerts(args: dict) -> dict:
    topic = args.get("topic", "innovation")
    return {
        "alerts": [
            {
                "topic": topic,
                "severity": "medium",
                "message": f"Trend velocity increased for {topic}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ]
    }

async def track_trends(args: dict) -> dict:
    keyword = args.get("keyword", "innovation")
    return {"keyword": keyword, "trend_score": 0.74, "direction": "up"}

app = create_mcp_app(
    "mcp_monitoring",
    "0.1.0",
    {
        "generate_alerts": generate_alerts,
        "track_trends": track_trends,
    },
)
