"""Main async run coordinator — orchestrates portal runs."""

import base64
import re
import shutil
from pathlib import Path

import httpx

import db.database as db
import core.tinyfish_client as tinyfish_client
from config.settings import MAX_RETRIES, SCREENSHOTS_DIR
from core.document_vault import DocumentVault
from core.profile import CompanyProfile, profile_to_dict
from db.models import PortalResult


def save_screenshot(data: str, save_dir: str, index: int) -> str:
    """Save a screenshot from URL, base64, or file path. Return saved path."""
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)
    dest = save_path / f"{index}.png"

    if data.startswith("http"):
        resp = httpx.get(data, timeout=30)
        dest.write_bytes(resp.content)
    elif data.startswith("data:image") or len(data) > 200:
        if data.startswith("data:image"):
            data = data.split(",", 1)[1]
        dest.write_bytes(base64.b64decode(data))
    else:
        src = Path(data)
        if src.exists():
            shutil.copy2(str(src), str(dest))

    return str(dest)


def extract_reference_id(text: str) -> str | None:
    """Try to extract a reference/acknowledgement ID from result text."""
    patterns = [
        r"(?:reference|ref|id|acknowledgement|ack)\w*\s*[=:]\s*([A-Za-z0-9\-/]+)",
        r"(?:reference|ref|id|acknowledgement|ack)\w+\s+([A-Za-z0-9\-/]{4,})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


async def run_single_portal(
    portal_url: str,
    portal_name: str,
    company_profile: CompanyProfile,
    document_vault: DocumentVault,
    run_id: str,
) -> PortalResult:
    """Run a single portal onboarding end-to-end."""
    db.insert_portal_result(
        PortalResult(run_id=run_id, portal_url=portal_url, portal_name=portal_name, status="running")
    )

    profile_dict = profile_to_dict(company_profile)
    goal = (
        f"Navigate to {portal_url}. Find the vendor, seller, or supplier "
        f"registration or onboarding form. Fill it completely with this company "
        f"data: {profile_dict}. Upload the GST certificate to any document "
        f"upload field you find. Complete all form pages and submit the form. "
        f"Return the confirmation reference number or any acknowledgement ID "
        f"shown after submission."
    )

    result = await tinyfish_client.run_agent(
        url=portal_url, goal=goal, context_data=profile_dict
    )

    screenshot_dir = f"{SCREENSHOTS_DIR}/{run_id}/{portal_name}"
    if result.screenshots:
        Path(screenshot_dir).mkdir(parents=True, exist_ok=True)
        for i, s in enumerate(result.screenshots):
            try:
                save_screenshot(s, screenshot_dir, i)
            except Exception:
                pass

    status = "submitted" if result.success else "failed"
    reference_id = extract_reference_id(result.result_text) if result.result_text else None

    db.update_portal_status(
        run_id=run_id,
        portal_url=portal_url,
        status=status,
        reference_id=reference_id,
        time_taken_seconds=result.duration_seconds,
        error_message=result.error,
        screenshot_dir=screenshot_dir if result.screenshots else None,
    )

    return PortalResult(
        run_id=run_id,
        portal_url=portal_url,
        portal_name=portal_name,
        status=status,
        reference_id=reference_id,
        time_taken_seconds=result.duration_seconds,
        error_message=result.error,
        screenshot_dir=screenshot_dir if result.screenshots else None,
    )


async def run_single_portal_with_retry(
    portal_url: str,
    portal_name: str,
    company_profile: CompanyProfile,
    document_vault: DocumentVault,
    run_id: str,
    max_retries: int | None = None,
) -> PortalResult:
    """Run a single portal with exponential backoff retry (F8)."""
    retries = max_retries if max_retries is not None else MAX_RETRIES
    db.create_run(run_id=run_id, portal_count=1)

    backoff = [5, 15, 45]
    last_error: str | None = None
    result: PortalResult | None = None

    for attempt in range(1, retries + 1):
        result = await run_single_portal(
            portal_url=portal_url,
            portal_name=portal_name,
            company_profile=company_profile,
            document_vault=document_vault,
            run_id=run_id,
        )
        result.retry_count = attempt - 1

        if result.status == "submitted":
            db.update_portal_status(
                run_id=run_id,
                portal_url=portal_url,
                status="submitted",
                retry_count=attempt - 1,
            )
            return result

        last_error = result.error_message or "unknown error"

        if last_error and any(kw in last_error.lower() for kw in ("auth", "login", "credential")):
            result.retry_count = attempt - 1
            result.last_error = last_error
            db.update_portal_status(
                run_id=run_id,
                portal_url=portal_url,
                status="failed",
                retry_count=attempt - 1,
                last_error=last_error,
            )
            return result

        if attempt < retries:
            import asyncio
            await asyncio.sleep(backoff[min(attempt - 1, len(backoff) - 1)])

    assert result is not None
    result.retry_count = retries
    result.last_error = last_error
    db.update_portal_status(
        run_id=run_id,
        portal_url=portal_url,
        status="failed",
        retry_count=retries,
        last_error=last_error,
    )
    return result
