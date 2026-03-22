"""VendorFlow AI — settings loader."""

import os

# Try Streamlit secrets first (for Streamlit Cloud), fall back to env vars
try:
    import streamlit as st

    def _get(key: str, default: str = "") -> str:
        try:
            return str(st.secrets[key])
        except Exception:
            return os.getenv(key, default)
except ImportError:
    def _get(key: str, default: str = "") -> str:
        return os.getenv(key, default)

# Load dotenv only for local development
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

TINYFISH_API_KEY: str = _get("TINYFISH_API_KEY", "")
TINYFISH_BASE_URL: str = _get(
    "TINYFISH_BASE_URL", "https://agent.tinyfish.ai/v1/automation/run-sse"
)
DB_PATH: str = _get("DB_PATH", "data/vendorflow.db")
BLUEPRINTS_DIR: str = _get("BLUEPRINTS_DIR", "data/blueprints")
SCREENSHOTS_DIR: str = _get("SCREENSHOTS_DIR", "data/screenshots")
REPORTS_DIR: str = _get("REPORTS_DIR", "data/reports")
UPLOADS_DIR: str = _get("UPLOADS_DIR", "data/uploads")
MAX_PARALLEL_AGENTS: int = int(_get("MAX_PARALLEL_AGENTS", "5"))
MAX_RETRIES: int = int(_get("MAX_RETRIES", "3"))

if not TINYFISH_API_KEY or TINYFISH_API_KEY == "your_api_key_here":
    print("WARNING: TINYFISH_API_KEY not set. Add it to your .env file.")

# Create data directories
for _dir in ["data", UPLOADS_DIR, BLUEPRINTS_DIR, SCREENSHOTS_DIR, REPORTS_DIR]:
    os.makedirs(_dir, exist_ok=True)
