"""Portal blueprint save/load — F11."""

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from config.settings import BLUEPRINTS_DIR
from db.models import PortalResult

import db.database as db


@dataclass
class FieldMapping:
    field_label: str
    maps_to_profile_key: str
    field_type: str  # "text" | "dropdown" | "file" | "date"


@dataclass
class PortalBlueprint:
    domain: str
    portal_name: str
    last_success_date: str
    known_fields: list[FieldMapping] = field(default_factory=list)
    required_documents: list[str] = field(default_factory=lambda: ["GST_CERT"])
    typical_page_count: int = 1
    known_edge_cases: list[str] = field(default_factory=list)
    success_count: int = 1


def extract_domain(url: str) -> str:
    """Extract domain from URL. e.g. 'https://seller.indiamart.com/xyz' → 'seller.indiamart.com'."""
    parsed = urlparse(url)
    return parsed.netloc or parsed.path.split("/")[0]


def save_blueprint(domain: str, portal_name: str, portal_result: PortalResult) -> str:
    """Save or update a portal blueprint after successful run."""
    if portal_result.status != "submitted":
        return ""

    blueprints_dir = Path(BLUEPRINTS_DIR)
    blueprints_dir.mkdir(parents=True, exist_ok=True)
    filepath = blueprints_dir / f"{domain}.json"

    if filepath.exists():
        existing = json.loads(filepath.read_text(encoding="utf-8"))
        existing["success_count"] = existing.get("success_count", 0) + 1
        existing["last_success_date"] = datetime.now(timezone.utc).isoformat()
        if existing.get("known_fields"):
            pass  # Don't overwrite if they exist
    else:
        existing = {
            "domain": domain,
            "portal_name": portal_name,
            "last_success_date": datetime.now(timezone.utc).isoformat(),
            "known_fields": [],
            "required_documents": ["GST_CERT"],
            "typical_page_count": 1,
            "known_edge_cases": [],
            "success_count": 1,
        }

    filepath.write_text(json.dumps(existing, indent=2), encoding="utf-8")

    try:
        db._get_conn().execute(
            """INSERT INTO blueprints (portal_domain, blueprint_path, created_at, last_used_at, success_count)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(portal_domain) DO UPDATE SET
               last_used_at = excluded.last_used_at,
               success_count = blueprints.success_count + 1""",
            (domain, str(filepath), existing["last_success_date"], existing["last_success_date"], existing["success_count"]),
        ).connection.commit()
    except Exception:
        pass

    return str(filepath)


def load_blueprint(domain: str) -> PortalBlueprint | None:
    """Load a portal blueprint from disk, or None if not found."""
    filepath = Path(BLUEPRINTS_DIR) / f"{domain}.json"
    if not filepath.exists():
        return None

    data = json.loads(filepath.read_text(encoding="utf-8"))
    fields = [FieldMapping(**f) for f in data.get("known_fields", [])]

    return PortalBlueprint(
        domain=data["domain"],
        portal_name=data["portal_name"],
        last_success_date=data["last_success_date"],
        known_fields=fields,
        required_documents=data.get("required_documents", ["GST_CERT"]),
        typical_page_count=data.get("typical_page_count", 1),
        known_edge_cases=data.get("known_edge_cases", []),
        success_count=data.get("success_count", 1),
    )


def blueprint_to_goal_hint(blueprint: PortalBlueprint) -> str:
    """Return a string to append to the TinyFish goal based on blueprint history."""
    if blueprint.known_fields:
        field_list = ", ".join(f.field_label for f in blueprint.known_fields)
        return (
            f"Note: This portal was previously completed successfully "
            f"{blueprint.success_count} time(s). Known form fields include: "
            f"{field_list}. If the layout has changed significantly, "
            f"ignore these hints and discover fields from scratch."
        )
    return (
        f"Note: This portal was previously completed successfully "
        f"{blueprint.success_count} time(s) on {blueprint.last_success_date}."
    )
