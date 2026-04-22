from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from backend.mcp_servers.common import create_mcp_app
from backend.services.reporting import ensure_reports_dir


def _write_csv(path: Path, idea_id: str) -> None:
    path.write_text('idea_id,artifact_type\n' + f'{idea_id},csv\n', encoding='utf-8')


def _write_pdf(path: Path, idea_id: str) -> None:
    content = f"%PDF-1.4\n1 0 obj<<>>endobj\n2 0 obj<< /Type /Catalog /Pages 3 0 R >>endobj\n3 0 obj<< /Type /Pages /Kids [4 0 R] /Count 1 >>endobj\n4 0 obj<< /Type /Page /Parent 3 0 R /MediaBox [0 0 300 144] /Contents 5 0 R >>endobj\n5 0 obj<< /Length 65 >>stream\nBT /F1 12 Tf 36 100 Td (Innovation Copilot Report: {idea_id}) Tj ET\nendstream endobj\nxref\n0 6\n0000000000 65535 f \ntrailer<< /Root 2 0 R /Size 6 >>\nstartxref\n0\n%%EOF"
    path.write_bytes(content.encode('utf-8'))


async def generate_report(args: dict) -> dict:
    idea_id = str(args['idea_id'])
    fmt = str(args.get('format', 'pdf')).lower()
    reports_dir = ensure_reports_dir()
    file_name = f'{uuid4()}.{fmt}'
    file_path = reports_dir / file_name

    if fmt == 'csv':
        _write_csv(file_path, idea_id)
    else:
        _write_pdf(file_path, idea_id)

    return {'artifact_path': str(file_path), 'format': fmt}


app = create_mcp_app(
    'mcp_report',
    '0.5.0',
    {'generate_report': generate_report},
)
