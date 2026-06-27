"""Torob scraper — priority #1 aggregator.

NOTE: selectors are placeholders based on Torob's typical search page layout.
Verify and adjust against the live DOM before production. Torob also exposes
an internal JSON API (api.torob.com) which is more robust than DOM scraping;
swap to that once you confirm reachability from the server.
"""
from typing import List
from urllib.parse import quote

from core.models import ProductResult
from core.scrapers.base import BaseScraper
from config import settings


class TorobScraper(BaseScraper):
    key = "torob"
    domain = "torob.com"

    async def search(self, query: str) -> List[ProductResult]:
        ctx = await self._new_context()
        page = await ctx.new_page()
        results: List[ProductResult] = []
        try:
            url = f"https://torob.com/search/?query={quote(query)}"
            await self._goto(page, url)

            # Wait for product cards to render.
            await page.wait_for_selector("a[href*='/p/']", timeout=settings.SCRAPE_TIMEOUT_MS)
            cards = await page.query_selector_all("a[href*='/p/']")

            for card in cards[: settings.MAX_RESULTS_PER_SITE]:
                try:
                    name_el = await card.query_selector("h2, .product-name, [class*='name']")
                    price_el = await card.query_selector("[class*='price']")
                    href = await card.get_attribute("href") or ""

                    name = (await name_el.inner_text()).strip() if name_el else ""
                    price = self._parse_price(await price_el.inner_text()) if price_el else None
                    link = href if href.startswith("http") else f"https://torob.com{href}"

                    if name:
                        results.append(ProductResult(
                            name=name, price=price, store="Torob (تجمیع‌کننده)",
                            link=link, source_site=self.key,
                        ))
                except Exception:
                    continue
            return results
        finally:
            await ctx.close()

    @staticmethod
    def _parse_price(text: str):
        digits = "".join(ch for ch in text if ch.isdigit())
        return int(digits) if digits else None
