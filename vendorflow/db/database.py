"""Database initialization, connection, and migrations."""

import sqlite3
from datetime import datetime, timezone

from config.settings import DB_PATH

from db.models import PortalResult


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables if they don't exist."""
    conn = _get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT UNIQUE NOT NULL,
            started_at TEXT NOT NULL,
            completed_at TEXT,
            portal_count INTEGER DEFAULT 0,
            success_count INTEGER DEFAULT 0,
            total_time_seconds REAL DEFAULT 0
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS portal_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            portal_url TEXT NOT NULL,
            portal_name TEXT NOT NULL,
            status TEXT DEFAULT 'queued',
            reference_id TEXT,
            time_taken_seconds REAL DEFAULT 0,
            error_message TEXT,
            screenshot_dir TEXT,
            retry_count INTEGER DEFAULT 0,
            last_error TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS blueprints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            portal_domain TEXT UNIQUE NOT NULL,
            blueprint_path TEXT NOT NULL,
            created_at TEXT NOT NULL,
            last_used_at TEXT,
            success_count INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def create_run(run_id: str, portal_count: int) -> None:
    """Insert a new row into runs table."""
    conn = _get_conn()
    conn.execute(
        "INSERT INTO runs (run_id, started_at, portal_count) VALUES (?, ?, ?)",
        (run_id, datetime.now(timezone.utc).isoformat(), portal_count),
    )
    conn.commit()
    conn.close()


def update_portal_status(run_id: str, portal_url: str, status: str, **kwargs) -> None:
    """Update portal_results row for given run_id + portal_url."""
    allowed = {
        "reference_id",
        "time_taken_seconds",
        "error_message",
        "screenshot_dir",
        "retry_count",
        "last_error",
    }
    fields = ["status = ?"]
    values: list = [status]

    for key, val in kwargs.items():
        if key in allowed:
            fields.append(f"{key} = ?")
            values.append(val)

    values.extend([run_id, portal_url])
    conn = _get_conn()
    conn.execute(
        f"UPDATE portal_results SET {', '.join(fields)} WHERE run_id = ? AND portal_url = ?",
        values,
    )
    conn.commit()
    conn.close()


def insert_portal_result(portal_result: PortalResult) -> None:
    """Insert a new portal_results row."""
    conn = _get_conn()
    conn.execute(
        """INSERT INTO portal_results
           (run_id, portal_url, portal_name, status, reference_id,
            time_taken_seconds, error_message, screenshot_dir,
            retry_count, last_error)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            portal_result.run_id,
            portal_result.portal_url,
            portal_result.portal_name,
            portal_result.status,
            portal_result.reference_id,
            portal_result.time_taken_seconds,
            portal_result.error_message,
            portal_result.screenshot_dir,
            portal_result.retry_count,
            portal_result.last_error,
        ),
    )
    conn.commit()
    conn.close()


def get_run_history() -> list[dict]:
    """Return all runs joined with their portal_results, ordered by started_at DESC."""
    conn = _get_conn()
    rows = conn.execute("""
        SELECT r.run_id, r.started_at, r.completed_at,
               r.portal_count, r.success_count, r.total_time_seconds,
               p.portal_url, p.portal_name, p.status,
               p.reference_id, p.time_taken_seconds, p.error_message,
               p.screenshot_dir, p.retry_count, p.last_error
        FROM runs r
        LEFT JOIN portal_results p ON r.run_id = p.run_id
        ORDER BY r.started_at DESC
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_blueprint_path(domain: str) -> str | None:
    """Return blueprint_path for given domain, or None."""
    conn = _get_conn()
    row = conn.execute(
        "SELECT blueprint_path FROM blueprints WHERE portal_domain = ?",
        (domain,),
    ).fetchone()
    conn.close()
    if row:
        return row["blueprint_path"]
    return None


init_db()
