"""Bale bot handler.

Bale exposes a Telegram-compatible Bot API at https://tapi.bale.ai/bot<TOKEN>/.
This uses raw HTTP (httpx) with long polling to stay dependency-light and
avoid version mismatches with the Telegram SDK.
"""
import asyncio
import logging

import httpx

from bot.core import handle_query, summary_caption
from config import settings

log = logging.getLogger("bale")
BASE = f"https://tapi.bale.ai/bot{settings.BALE_TOKEN}"


async def _api(client: httpx.AsyncClient, method: str, **params):
    r = await client.post(f"{BASE}/{method}", data=params, timeout=60)
    r.raise_for_status()
    return r.json()


async def _send_doc(client: httpx.AsyncClient, chat_id: int, path):
    with open(path, "rb") as f:
        files = {"document": (path.name, f)}
        r = await client.post(f"{BASE}/sendDocument",
                              data={"chat_id": chat_id}, files=files, timeout=120)
        r.raise_for_status()


async def _process(client: httpx.AsyncClient, chat_id: int, text: str):
    await _api(client, "sendMessage", chat_id=chat_id,
               text="🔍 در حال جستجو... چند لحظه صبر کن.")
    try:
        excel_path, summary, errors = await handle_query(text)
        await _api(client, "sendMessage", chat_id=chat_id,
                   text=summary_caption(text, summary))
        if summary["count"] > 0:
            await _send_doc(client, chat_id, excel_path)
        if errors:
            log.warning("Scraper errors for '%s': %s", text, errors)
    except Exception:
        log.exception("handle_query failed")
        await _api(client, "sendMessage", chat_id=chat_id,
                   text="خطایی رخ داد. لطفاً دوباره تلاش کن.")


async def run():
    logging.basicConfig(level=logging.INFO)
    offset = 0
    async with httpx.AsyncClient() as client:
        log.info("Bale bot started.")
        while True:
            try:
                data = await _api(client, "getUpdates", offset=offset, timeout=30)
                for upd in data.get("result", []):
                    offset = upd["update_id"] + 1
                    msg = upd.get("message")
                    if not msg or "text" not in msg:
                        continue
                    chat_id = msg["chat"]["id"]
                    text = msg["text"]
                    if text.startswith("/start"):
                        await _api(client, "sendMessage", chat_id=chat_id,
                                   text="سلام! 👋 نام محصول رو بفرست تا قیمت‌ها رو پیدا کنم.")
                    else:
                        asyncio.create_task(_process(client, chat_id, text))
            except Exception:
                log.exception("polling error")
                await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(run())
