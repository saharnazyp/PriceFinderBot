"""Central configuration. Loads from environment with sane defaults."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Messaging platform tokens ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
BALE_TOKEN = os.getenv("BALE_TOKEN", "")

# --- Server context ---
# Server has an IRANIAN IP: Iranian e-commerce sites are reachable directly,
# but Groq/Gemini/OpenRouter are NOT reachable. Keep LLM optional.
SERVER_IP_REGION = os.getenv("SERVER_IP_REGION", "iran")  # "iran" | "foreign"
LLM_ENABLED = os.getenv("LLM_ENABLED", "false").lower() == "true"

# --- LLM provider keys (only used when LLM_ENABLED and a route is reachable) ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# --- Scraping ---
SCRAPE_TIMEOUT_MS = int(os.getenv("SCRAPE_TIMEOUT_MS", "30000"))
MAX_RESULTS_PER_SITE = int(os.getenv("MAX_RESULTS_PER_SITE", "15"))
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
CONCURRENT_SCRAPERS = int(os.getenv("CONCURRENT_SCRAPERS", "4"))

# --- Output ---
OUTPUT_DIR = BASE_DIR / "data" / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
