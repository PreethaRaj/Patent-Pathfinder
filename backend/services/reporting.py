from __future__ import annotations

from pathlib import Path

from backend.core.config import settings


def ensure_reports_dir() -> Path:
    reports_dir = Path(settings.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    return reports_dir
