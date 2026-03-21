"""TinyFish client tests — mocked httpx calls."""

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from core.tinyfish_client import TinyFishResult, run_agent


def _make_sse_events(events: list[dict]) -> list[str]:
    """Convert event dicts to SSE-formatted lines."""
    return [f"data: {json.dumps(e)}" for e in events]


class MockSSEStream:
    """Mock for httpx streaming response with SSE lines."""

    def __init__(self, status_code: int = 200, lines: list[str] | None = None):
        self.status_code = status_code
        self._lines = lines or []

    async def aiter_lines(self):
        for line in self._lines:
            yield line

    async def aread(self):
        return b"mock error body"

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass


class MockClient:
    """Mock for httpx.AsyncClient."""

    def __init__(self, stream_obj: MockSSEStream):
        self._stream_obj = stream_obj

    def stream(self, method, url, **kwargs):
        return self._stream_obj

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass


@pytest.mark.asyncio
async def test_successful_response():
    """Mock returns valid SSE stream with a 'COMPLETE' event → success=True."""
    events = [
        {"type": "MESSAGE", "content": "Navigating to page..."},
        {"type": "COMPLETE", "result": "The title is Google"},
    ]
    lines = _make_sse_events(events)
    stream = MockSSEStream(status_code=200, lines=lines)
    mock_client = MockClient(stream)

    with patch("core.tinyfish_client.httpx.AsyncClient", return_value=mock_client):
        result = await run_agent(url="https://www.google.com", goal="Get title")

    assert result.success is True
    assert result.result_text == "The title is Google"
    assert len(result.steps) == 2


@pytest.mark.asyncio
async def test_timeout():
    """Mock raises httpx.TimeoutException → success=False, 'timeout' in error."""
    mock_client = MagicMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.stream.side_effect = httpx.TimeoutException("timed out")

    with patch("core.tinyfish_client.httpx.AsyncClient", return_value=mock_client):
        result = await run_agent(url="https://www.google.com", goal="Get title")

    assert result.success is False
    assert "timeout" in result.error


@pytest.mark.asyncio
async def test_connection_error():
    """Mock raises httpx.ConnectError → success=False."""
    mock_client = MagicMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.stream.side_effect = httpx.ConnectError("refused")

    with patch("core.tinyfish_client.httpx.AsyncClient", return_value=mock_client):
        result = await run_agent(url="https://www.google.com", goal="Get title")

    assert result.success is False
    assert result.error is not None


@pytest.mark.asyncio
async def test_non_200_response():
    """Mock returns status 401 → success=False, '401' in error."""
    stream = MockSSEStream(status_code=401, lines=[])
    mock_client = MockClient(stream)

    with patch("core.tinyfish_client.httpx.AsyncClient", return_value=mock_client):
        result = await run_agent(url="https://www.google.com", goal="Get title")

    assert result.success is False
    assert "401" in result.error


@pytest.mark.asyncio
async def test_result_structure():
    """Successful mock response → all fields exist on TinyFishResult."""
    events = [
        {"type": "MESSAGE", "content": "Step 1"},
        {"type": "COMPLETE", "result": "Done"},
    ]
    lines = _make_sse_events(events)
    stream = MockSSEStream(status_code=200, lines=lines)
    mock_client = MockClient(stream)

    with patch("core.tinyfish_client.httpx.AsyncClient", return_value=mock_client):
        result = await run_agent(url="https://example.com", goal="Test")

    assert isinstance(result, TinyFishResult)
    assert hasattr(result, "success")
    assert hasattr(result, "result_text")
    assert hasattr(result, "screenshots")
    assert hasattr(result, "steps")
    assert hasattr(result, "duration_seconds")
    assert hasattr(result, "error")
    assert isinstance(result.screenshots, list)
    assert isinstance(result.steps, list)
    assert isinstance(result.duration_seconds, float)
