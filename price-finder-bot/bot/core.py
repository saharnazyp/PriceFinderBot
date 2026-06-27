"""Platform-agnostic core: takes a query, returns an Excel path + summary.

Both Telegram and Bale handlers call `handle_query`.
"""
from pathlib import Path
from typing import Tuple

from core.aggregator.aggregate import aggregate, price_summary
from core.excel.builder import build_excel
from core.scrapers.engine import run_search


async def handle_query(query: str) -> Tuple[Path, dict, list]:
    """Returns (excel_path, summary_dict, errors)."""
    query = query.strip()
    response = await run_search(query)
    results = aggregate(response)
    summary = price_summary(results)
    excel_path = build_excel(query, results)
    return excel_path, summary, response.errors


def summary_caption(query: str, summary: dict) -> str:
    if summary["count"] == 0:
        return f"برای «{query}» نتیجه‌ای پیدا نشد. 😔"
    return (
        f"✅ نتایج «{query}» آماده شد.\n"
        f"تعداد: {summary['count']} مورد\n"
        f"کمترین قیمت: {summary['min']:,} تومان\n"
        f"بیشترین قیمت: {summary['max']:,} تومان\n"
        f"میانگین: {summary['avg']:,} تومان"
    )
