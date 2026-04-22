from fastapi import APIRouter

from backend.models.schemas import IdeaCreate, IdeaResponse
from backend.services.orchestration import Orchestrator

router = APIRouter(tags=["ideas"])


@router.post("/ideas", response_model=IdeaResponse)
async def create_idea(payload: IdeaCreate) -> IdeaResponse:
    orchestrator = Orchestrator()
    result = await orchestrator.analyze_idea(payload)
    return IdeaResponse.model_validate(result)


@router.post("/ideas/analyze", response_model=IdeaResponse)
async def analyze_sample_idea(payload: dict) -> IdeaResponse:
    orchestrator = Orchestrator()
    idea = IdeaCreate(
        title=payload.get("title", "Untitled Idea"),
        problem_statement=payload.get("input_text") or payload.get("idea") or payload.get("problem_statement", ""),
        domain=payload.get("domain", "general"),
        objectives=payload.get("objectives", []),
        constraints=payload.get("constraints", []),
        tags=payload.get("tags", []),
    )
    result = await orchestrator.analyze_idea(idea, source_override=payload.get("source"))
    return IdeaResponse.model_validate(result)