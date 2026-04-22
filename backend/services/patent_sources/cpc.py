from __future__ import annotations

import re
from collections import Counter
from typing import Iterable

_CPC_RE = re.compile(r'^[A-HY][0-9]{2}[A-Z]?[0-9]*/?[0-9]*$')


def normalize_cpc(code: str) -> str:
    return (code or '').strip().replace(' ', '').upper()


def select_top_cpcs(results: Iterable[dict], max_codes: int = 5) -> list[str]:
    counter: Counter[str] = Counter()
    for item in results:
        for raw in item.get('cpc_codes', []) or []:
            code = normalize_cpc(raw)
            if code:
                counter[code] += 1
    selected = [code for code, _ in counter.most_common(max_codes)]
    return selected


def suggest_cpcs_from_text(text: str) -> list[str]:
    lowered = text.lower()
    suggestions: list[str] = []
    if any(token in lowered for token in ['inventory', 'warehouse', 'stockout', 'erp', 'logistics']):
        suggestions.append('G06Q10/08')
    if any(token in lowered for token in ['camera', 'vision', 'shelf', 'image', 'object recognition']):
        suggestions.append('G06V20/52')
    if any(token in lowered for token in ['prediction', 'neural', 'ai', 'machine learning', 'model']):
        suggestions.append('G06N3/08')
    if any(token in lowered for token in ['audio', 'microphone', 'sound']):
        suggestions.append('G10L25/63')
    return suggestions[:5]
