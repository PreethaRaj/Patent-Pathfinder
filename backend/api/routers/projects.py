from datetime import datetime, timezone

from fastapi import APIRouter

from backend.models.schemas import ProjectSummary

router = APIRouter(tags=["projects"])

@router.get("/projects", response_model=list[ProjectSummary])
async def list_projects() -> list[ProjectSummary]:
    return [
        ProjectSummary(
            project_id="demo-project-1",
            title="Bio-based packaging concept",
            domain="materials",
            status="active",
            updated_at=datetime.now(timezone.utc),
        )
    ]
