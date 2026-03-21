"""Layout-change resilience mode — F12."""

from core.blueprint import PortalBlueprint, blueprint_to_goal_hint


def build_resilient_goal(
    portal_url: str,
    base_goal: str,
    blueprint: PortalBlueprint | None,
) -> str:
    """Enhance goal string with blueprint hints or exploration notes."""
    parts = [base_goal]

    if blueprint:
        parts.append(blueprint_to_goal_hint(blueprint))
    else:
        parts.append(
            "Note: This portal has not been seen before. "
            "Carefully explore all form fields and pages before filling. "
            "Do not assume field positions."
        )

    parts.append(
        "If you encounter a CAPTCHA, describe it and stop. "
        "If the page layout looks completely different from what is described, "
        "use visual exploration to find the registration form."
    )

    return " ".join(parts)
