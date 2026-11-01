"""Central configuration. Secrets are read from env vars or Streamlit secrets only."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

APP_NAME = "Nexus AI"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DB_PATH = Path(os.getenv("NEXUS_DB_PATH") or ROOT / "data" / "nexus.db")
DEFAULT_MODEL = os.getenv("NEXUS_DEFAULT_MODEL", "openai/gpt-4o-mini")

# Used only if the live model list cannot be fetched.
FALLBACK_MODELS = [
    "openai/gpt-4o-mini",
    "openai/gpt-4o",
    "anthropic/claude-3.5-haiku",
    "google/gemini-2.0-flash-001",
    "meta-llama/llama-3.3-70b-instruct",
    "deepseek/deepseek-chat",
]

DEFAULT_SYSTEM_PROMPT = (
    "You are Nexus AI, a sharp, friendly assistant. Answer clearly and concisely, "
    "use Markdown for structure, and put code in fenced code blocks."
)

DEFAULT_SETTINGS = {
    "model": DEFAULT_MODEL,
    "temperature": 0.7,
    "max_tokens": 1024,
    "system_prompt": DEFAULT_SYSTEM_PROMPT,
}


def get_api_key() -> str | None:
    """Env var / .env first (local), then Streamlit secrets (cloud)."""
    key = os.getenv("OPENROUTER_API_KEY")
    if key and key.strip():
        return key.strip()
    try:
        import streamlit as st

        value = st.secrets.get("OPENROUTER_API_KEY")
        if value and str(value).strip():
            return str(value).strip()
    except Exception:  # no secrets file configured
        pass
    return None
