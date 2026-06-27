"""Optional LLM fallback chain: Groq -> Gemini -> OpenRouter.

IMPORTANT: On the current server (Iranian IP), none of these are reachable.
LLM_ENABLED defaults to False, so the bot runs fully on keyword search.
Wire a proxy or a foreign-IP route before enabling.

This module is kept isolated so the core never depends on it.
"""
import logging
from typing import Optional

from config import settings

log = logging.getLogger("llm")


class LLMRouter:
    def __init__(self):
        self.enabled = settings.LLM_ENABLED

    async def normalize_query(self, raw: str) -> str:
        """Clean/expand a user query. Falls back to identity if LLM disabled."""
        if not self.enabled:
            return raw.strip()
        for provider in (self._groq, self._gemini, self._openrouter):
            try:
                out = await provider(raw)
                if out:
                    return out
            except Exception as e:  # noqa: BLE001
                log.warning("LLM provider failed: %s", e)
                continue
        return raw.strip()

    async def _groq(self, text: str) -> Optional[str]:
        raise NotImplementedError("wire Groq client when reachable")

    async def _gemini(self, text: str) -> Optional[str]:
        raise NotImplementedError("wire Gemini client when reachable")

    async def _openrouter(self, text: str) -> Optional[str]:
        raise NotImplementedError("wire OpenRouter client when reachable")
