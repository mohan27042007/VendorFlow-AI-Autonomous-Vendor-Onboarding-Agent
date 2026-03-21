"""Database models — run history, portal status, blueprints."""

from dataclasses import dataclass, field


@dataclass
class PortalResult:
    run_id: str
    portal_url: str
    portal_name: str
    status: str = "queued"
    reference_id: str | None = None
    time_taken_seconds: float = 0.0
    error_message: str | None = None
    screenshot_dir: str | None = None
    retry_count: int = 0
    last_error: str | None = None


@dataclass
class RunSummary:
    run_id: str
    started_at: str
    completed_at: str | None = None
    portal_count: int = 0
    success_count: int = 0
    total_time_seconds: float = 0.0
