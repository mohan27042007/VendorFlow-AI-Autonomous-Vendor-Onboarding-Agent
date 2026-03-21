"""TinyFish Web Agent API wrapper — F3."""

import json
import time
from dataclasses import dataclass, field

import httpx

from config.settings import TINYFISH_API_KEY, TINYFISH_BASE_URL


@dataclass
class TinyFishResult:
    success: bool = False
    result_text: str = ""
    screenshots: list[str] = field(default_factory=list)
    steps: list[dict] = field(default_factory=list)
    duration_seconds: float = 0.0
    error: str | None = None


async def run_agent(
    url: str,
    goal: str,
    context_data: dict | None = None,
    files: list | None = None,
) -> TinyFishResult:
    """Run a TinyFish web agent session and stream the SSE response."""
    start = time.monotonic()
    result = TinyFishResult()

    body: dict = {
        "url": url,
        "goal": goal,
        "context": context_data,
        "proxy_config": {"enabled": False},
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": TINYFISH_API_KEY,
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream(
                "POST", TINYFISH_BASE_URL, json=body, headers=headers
            ) as response:
                if response.status_code != 200:
                    body_text = await response.aread()
                    result.error = (
                        f"HTTP {response.status_code}: {body_text.decode()[:500]}"
                    )
                    result.duration_seconds = time.monotonic() - start
                    return result

                async for line in response.aiter_lines():
                    if not line.startswith("data: "):
                        continue

                    raw = line[6:]
                    try:
                        event = json.loads(raw)
                    except json.JSONDecodeError:
                        continue

                    event_type = event.get("type", "").upper()

                    if event_type == "COMPLETE":
                        result.success = True
                        result.result_text = str(event.get("result", ""))
                        result.steps.append(event)

                    elif event_type == "ERROR":
                        result.success = False
                        result.error = event.get("content", "Unknown agent error")
                        result.steps.append(event)

                    elif event_type == "MESSAGE":
                        result.steps.append(event)

                        content = event.get("content", "")
                        if isinstance(content, dict) and content.get("screenshot"):
                            result.screenshots.append(content["screenshot"])

                    else:
                        result.steps.append(event)

    except httpx.TimeoutException:
        result.error = "timeout after 120s"
    except httpx.ConnectError:
        result.error = "connection failed"
    except Exception as exc:
        result.error = str(exc)

    result.duration_seconds = time.monotonic() - start
    return result


if __name__ == "__main__":
    import asyncio
    from config.settings import TINYFISH_API_KEY

    if not TINYFISH_API_KEY or TINYFISH_API_KEY == "your_api_key_here":
        print("No API key set. Add TINYFISH_API_KEY to your .env file.")
    else:
        result = asyncio.run(
            run_agent(
                url="https://www.google.com",
                goal="What is the title of this page?",
            )
        )
        print(result)
