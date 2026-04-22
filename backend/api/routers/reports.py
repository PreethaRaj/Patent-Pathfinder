from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from backend.core.config import settings
from backend.models.schemas import ReportRequest, ReportResponse
from backend.services.mcp_client import MCPClient

router = APIRouter(tags=['reports'])


@router.post('/reports', response_model=ReportResponse)
async def generate_report(payload: ReportRequest) -> ReportResponse:
    client = MCPClient(settings.mcp_report_url)
    result = await client.command('generate_report', payload.model_dump())
    artifact_path = str(result['artifact_path'])
    file_name = Path(artifact_path).name
    download_url = f"{settings.public_api_base_url.rstrip('/')}/api/v1/reports/download/{file_name}"
    return ReportResponse(artifact_path=artifact_path, format=result['format'], download_url=download_url)


@router.get('/reports/download/{file_name}')
async def download_report(file_name: str):
    reports_dir = Path(settings.reports_dir)
    file_path = reports_dir / Path(file_name).name
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail='file not found')
    media_type = 'application/pdf' if file_path.suffix.lower() == '.pdf' else 'text/csv'
    return FileResponse(path=file_path, filename=file_path.name, media_type=media_type)
