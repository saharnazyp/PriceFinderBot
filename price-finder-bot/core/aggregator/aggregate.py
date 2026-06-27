"""Aggregates raw scraper output: filter invalid, dedup, sort by price."""
from typing import List

from core.models import ProductResult, SearchResponse


def aggregate(response: SearchResponse) -> List[ProductResult]:
    valid = [r for r in response.results if r.is_valid()]

    # Dedup on (normalized name, store, price).
    seen = set()
    unique: List[ProductResult] = []
    for r in valid:
        sig = (_norm(r.name), _norm(r.store), r.price)
        if sig not in seen:
            seen.add(sig)
            unique.append(r)

    # Sort low -> high price.
    unique.sort(key=lambda r: r.price)
    return unique


def price_summary(results: List[ProductResult]) -> dict:
    if not results:
        return {"min": None, "max": None, "avg": None, "count": 0}
    prices = [r.price for r in results]
    return {
        "min": min(prices),
        "max": max(prices),
        "avg": round(sum(prices) / len(prices)),
        "count": len(results),
    }


def _norm(s: str) -> str:
    return " ".join(s.lower().split())
