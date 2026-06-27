"""Base scraper. Each site scraper inherits and implements `search()`."""
import asyncio
import random
from abc import ABC, abstractmethod
from typing import List

from playwright.async_api import Browser, BrowserContext, Page

from config import settings
from core.models import ProductResult

_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


class BaseScraper(ABC):
    """Subclasses set `key` and `domain`, implement `search()`."""

    key: str = ""
    domain: str = ""

    def __init__(self, browser: Browser):
        self.browser = browser

    async def _new_context(self) -> BrowserContext:
        return await self.browser.new_context(
            user_agent=_UA,
            locale="fa-IR",
            viewport={"width": 1366, "height": 768},
            extra_http_headers={"Accept-Language": "fa-IR,fa;q=0.9,en;q=0.8"},
        )

    async def _human_pause(self, lo: float = 0.4, hi: float = 1.3):
        await asyncio.sleep(random.uniform(lo, hi))

    async def _goto(self, page: Page, url: str):
        await page.goto(url, timeout=settings.SCRAPE_TIMEOUT_MS,
                        wait_until="domcontentloaded")
        await self._human_pause()

    @abstractmethod
    async def search(self, query: str) -> List[ProductResult]:
        """Return up to MAX_RESULTS_PER_SITE results for `query`."""
        ...

    async def safe_search(self, query: str):
        """Wrapper that never raises; returns (results, error)."""
        try:
            results = await self.search(query)
            return results[: settings.MAX_RESULTS_PER_SITE], None
        except Exception as e:  # noqa: BLE001
            return [], f"{self.key}: {type(e).__name__}: {e}"
