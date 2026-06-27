"""Scraper registry + concurrent orchestration.

Add new site scrapers to SCRAPER_CLASSES as you implement them.
The engine launches one shared Playwright browser and runs scrapers
in priority order with a concurrency cap.
"""
import asyncio
from typing import List, Type

from playwright.async_api import async_playwright

from config import settings
from core.models import ProductResult, SearchResponse
from core.scrapers.base import BaseScraper
from core.scrapers.torob import TorobScraper

# Register implemented scrapers here. Ordered by priority.
SCRAPER_CLASSES: List[Type[BaseScraper]] = [
    TorobScraper,
    # DigikalaScraper,
    # EmallsScraper,
    # ... add the rest of the 20 sites
]


async def run_search(query: str) -> SearchResponse:
    response = SearchResponse(query=query)
    sem = asyncio.Semaphore(settings.CONCURRENT_SCRAPERS)

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=settings.HEADLESS)
        scrapers = [cls(browser) for cls in SCRAPER_CLASSES]

        async def _run(scraper: BaseScraper):
            async with sem:
                results, error = await scraper.safe_search(query)
                if error:
                    response.errors.append(error)
                return results

        all_results = await asyncio.gather(*(_run(s) for s in scrapers))
        await browser.close()

    for batch in all_results:
        response.results.extend(batch)
    return response
