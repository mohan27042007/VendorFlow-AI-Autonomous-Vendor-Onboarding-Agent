"""Orchestrator tests — mocked TinyFish calls."""

import uuid
from unittest.mock import AsyncMock, patch

import pytest

from core.document_vault import DocumentVault
from core.orchestrator import run_batch, run_single_portal, run_single_portal_with_retry
from core.profile import load_profile
from core.scoped_vault import get_scoped_data
from core.tinyfish_client import TinyFishResult


@pytest.fixture
def profile():
    return load_profile("data/sample_profile.json")


@pytest.fixture
def vault(tmp_path):
    return DocumentVault(uploads_dir=str(tmp_path))


def _success_result(result_text="Reference ID: ABC123"):
    return TinyFishResult(
        success=True,
        result_text=result_text,
        duration_seconds=5.0,
    )


def _fail_result(error="something went wrong"):
    return TinyFishResult(
        success=False,
        error=error,
        duration_seconds=3.0,
    )


@pytest.mark.asyncio
async def test_run_single_portal_success(profile, vault):
    """Mock run_agent returns success=True → status == submitted."""
    with patch("core.orchestrator.save_blueprint"), \
         patch("core.orchestrator.tinyfish_client.run_agent", new_callable=AsyncMock) as mock:
        mock.return_value = _success_result()
        result = await run_single_portal(
            portal_url="https://seller.example.com",
            portal_name="Example",
            company_profile=profile,
            document_vault=vault,
            run_id=str(uuid.uuid4()),
        )
    assert result.status == "submitted"
    assert result.reference_id == "ABC123"


@pytest.mark.asyncio
async def test_run_single_portal_failure(profile, vault):
    """Mock run_agent returns success=False → status == failed."""
    with patch("core.orchestrator.tinyfish_client.run_agent", new_callable=AsyncMock) as mock:
        mock.return_value = _fail_result()
        result = await run_single_portal(
            portal_url="https://seller.example.com",
            portal_name="Example",
            company_profile=profile,
            document_vault=vault,
            run_id=str(uuid.uuid4()),
        )
    assert result.status == "failed"


@pytest.mark.asyncio
async def test_retry_on_failure(profile, vault):
    """Mock fails twice then succeeds → status == submitted, retry_count == 2."""
    call_count = 0

    async def mock_run_agent(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            return _fail_result("temporary error")
        return _success_result()

    with patch("core.orchestrator.save_blueprint"), \
         patch("core.orchestrator.tinyfish_client.run_agent", side_effect=mock_run_agent):
        result = await run_single_portal_with_retry(
            portal_url="https://seller.example.com",
            portal_name="Example",
            company_profile=profile,
            document_vault=vault,
            run_id=str(uuid.uuid4()),
            max_retries=3,
        )
    assert result.status == "submitted"
    assert result.retry_count == 2


@pytest.mark.asyncio
async def test_no_retry_on_auth_error(profile, vault):
    """Mock returns auth error → only tried once, no retries."""
    call_count = 0

    async def mock_run_agent(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        return _fail_result("authentication failed: invalid credentials")

    with patch("core.orchestrator.tinyfish_client.run_agent", side_effect=mock_run_agent):
        result = await run_single_portal_with_retry(
            portal_url="https://seller.example.com",
            portal_name="Example",
            company_profile=profile,
            document_vault=vault,
            run_id=str(uuid.uuid4()),
            max_retries=3,
        )
    assert call_count == 1
    assert result.status == "failed"


@pytest.mark.asyncio
async def test_run_batch_two_portals(profile, vault):
    """Mock run_single_portal_with_retry returns success for both → success_count == 2."""
    with patch("core.orchestrator.run_single_portal_with_retry", new_callable=AsyncMock) as mock:
        mock.return_value = _success_result().__dict__ | {
            "run_id": "batch-test",
            "portal_url": "https://example.com",
            "portal_name": "Example",
            "status": "submitted",
            "retry_count": 0,
            "last_error": None,
        }
        from db.models import PortalResult
        mock.return_value = PortalResult(
            run_id="batch-test",
            portal_url="https://example.com",
            portal_name="Example",
            status="submitted",
            reference_id="ABC123",
            time_taken_seconds=5.0,
        )
        portals = [
            {"url": "https://seller.example.com", "name": "Portal1"},
            {"url": "https://seller2.example.com", "name": "Portal2"},
        ]
        result = await run_batch(portals, profile, vault)
    assert result.success_count == 2
    assert len(result.portal_results) == 2


@pytest.mark.asyncio
async def test_run_batch_partial_failure(profile, vault):
    """First portal success, second portal failure → success_count=1, fail_count=1."""
    call_count = 0

    async def mock_retry(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        from db.models import PortalResult
        if call_count == 1:
            return PortalResult(
                run_id="batch-test", portal_url="p1", portal_name="P1", status="submitted"
            )
        return PortalResult(
            run_id="batch-test", portal_url="p2", portal_name="P2", status="failed", error_message="err"
        )

    with patch("core.orchestrator.run_single_portal_with_retry", side_effect=mock_retry):
        portals = [
            {"url": "https://p1.example.com", "name": "P1"},
            {"url": "https://p2.example.com", "name": "P2"},
        ]
        result = await run_batch(portals, profile, vault)
    assert result.success_count == 1
    assert result.fail_count == 1


def test_get_scoped_data_marketplace(profile, vault):
    """IndiaMART URL → tan NOT in result, gstin IN result."""
    scoped = get_scoped_data("https://seller.indiamart.com", profile, vault)
    assert "tan" not in scoped
    assert "gstin" in scoped
    assert "pan" in scoped


def test_get_scoped_data_government(profile, vault):
    """gem.gov.in URL → tan IN result."""
    scoped = get_scoped_data("https://mkp.gem.gov.in", profile, vault)
    assert "tan" in scoped
    assert "cin" in scoped
    assert "gstin" in scoped
