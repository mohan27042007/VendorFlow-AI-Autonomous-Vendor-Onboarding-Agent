"""VendorFlow AI — settings loader."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TINYFISH_API_KEY: str = os.getenv("TINYFISH_API_KEY", "")
TINYFISH_BASE_URL: str = os.getenv(
    "TINYFISH_BASE_URL", "https://agent.tinyfish.ai/v1/automation/run-sse"
)
DB_PATH: str = os.getenv("DB_PATH", "data/vendorflow.db")
BLUEPRINTS_DIR: str = os.getenv("BLUEPRINTS_DIR", "data/blueprints")
SCREENSHOTS_DIR: str = os.getenv("SCREENSHOTS_DIR", "data/screenshots")
REPORTS_DIR: str = os.getenv("REPORTS_DIR", "data/reports")
UPLOADS_DIR: str = os.getenv("UPLOADS_DIR", "data/uploads")
MAX_PARALLEL_AGENTS: int = int(os.getenv("MAX_PARALLEL_AGENTS", "5"))
MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))

if not TINYFISH_API_KEY or TINYFISH_API_KEY == "your_api_key_here":
    print("WARNING: TINYFISH_API_KEY not set. Add it to your .env file.")

for _dir in [UPLOADS_DIR, BLUEPRINTS_DIR, SCREENSHOTS_DIR, REPORTS_DIR]:
    Path(_dir).mkdir(parents=True, exist_ok=True)
