"""Shared data models passed between scrapers, aggregator, and excel builder."""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ProductResult:
    name: str
    price: Optional[int]            # in Tomans; None if unavailable
    store: str                     # store / seller name
    link: str                      # purchase URL
    in_stock: bool = True
    rating: Optional[float] = None # seller rating 0-5
    source_site: str = ""          # which scraper produced this

    def is_valid(self) -> bool:
        return bool(self.name) and self.price is not None and self.price > 0


@dataclass
class SearchResponse:
    query: str
    results: list = field(default_factory=list)  # list[ProductResult]
    errors: list = field(default_factory=list)   # list[str] per-site failures
