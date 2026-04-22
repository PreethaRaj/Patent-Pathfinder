from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class PatentSearchResult:
    id: str
    title: str
    abstract: str = ''
    snippets: list[str] = field(default_factory=list)
    cpc_codes: list[str] = field(default_factory=list)
    score: float = 0.0
    source: str = 'unknown'
    url: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)
