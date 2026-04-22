from __future__ import annotations

from urllib.parse import quote_plus

import httpx
from bs4 import BeautifulSoup

from backend.core.config import settings
from backend.services.patent_sources.base import PatentSearchResult
from backend.services.patent_sources.cache import cache_get, cache_set, make_cache_key


class GooglePatentsSource:
    def __init__(self) -> None:
        self.base_url = settings.google_patents_base_url.rstrip('/')
        self.timeout = settings.google_patents_timeout_seconds

    async def search(self, query: str, limit: int = 10) -> list[PatentSearchResult]:
        cache_key = make_cache_key('google.search', {'query': query, 'limit': limit})
        cached = cache_get(cache_key)
        if cached is not None:
            return cached
        url = f'{self.base_url}/?q={quote_plus(query)}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; innovation-copilot/1.0)',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            html = response.text
        soup = BeautifulSoup(html, 'lxml')
        results: list[PatentSearchResult] = []
        seen: set[str] = set()
        for anchor in soup.select('a[href*="/patent/"]'):
            href = anchor.get('href', '')
            title = anchor.get_text(' ', strip=True)
            if not href or not title:
                continue
            patent_id = href.split('/patent/')[-1].split('/')[0]
            if not patent_id or patent_id in seen:
                continue
            seen.add(patent_id)
            results.append(
                PatentSearchResult(
                    id=patent_id,
                    title=title[:300],
                    abstract='',
                    snippets=[],
                    cpc_codes=[],
                    score=0.25,
                    source='google',
                    url=f'{self.base_url}/patent/{patent_id}',
                )
            )
            if len(results) >= limit:
                break
        cache_set(cache_key, results)
        return results

    async def search_by_cpc(self, query: str, cpc_codes: list[str], limit: int = 10) -> list[PatentSearchResult]:
        full_query = query
        if cpc_codes:
            full_query = f"{query} " + ' '.join([f'CPC={code}' for code in cpc_codes])
        return await self.search(full_query, limit=limit)
