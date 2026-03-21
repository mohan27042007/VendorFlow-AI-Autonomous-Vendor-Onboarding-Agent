"""Orchestrator tests — mocked TinyFish calls."""

import uuid
from unittest.mock import AsyncMock, patch

import pytest

from core.document_vault import DocumentVault
from core.orchestrator import run_single_portal, run_single_portal_with_retry
from core.profile import load_profile
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
    with patch("core.orchestrator.tinyfish_client.run_agent", new_callable=AsyncMock) as mock:
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

    with patch("core.orchestrator.tinyfish_client.run_agent", side_effect=mock_run_agent):
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
