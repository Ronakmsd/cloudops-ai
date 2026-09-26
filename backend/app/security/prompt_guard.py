from dataclasses import dataclass


@dataclass(frozen=True)
class GuardDecision:
    allowed: bool
    reason: str


BLOCKED_PATTERNS = (
    "ignore previous instructions",
    "ignore all previous instructions",
    "ignore your instructions",
    "bypass security",
    "disable security",
    "reveal system prompt",
    "reveal hidden instructions",
    "show your system prompt",
    "override security",
)


def check_prompt_safety(text: str) -> GuardDecision:
    """
    Basic defense-in-depth guard for obvious prompt-injection attempts.

    This guard does not replace authorization or SQL validation.
    It provides an additional policy layer before sensitive actions.
    """

    normalized = text.strip().lower()

    if not normalized:
        return GuardDecision(
            allowed=False,
            reason="Empty request is not allowed.",
        )

    for pattern in BLOCKED_PATTERNS:
        if pattern in normalized:
            return GuardDecision(
                allowed=False,
                reason="Request contains a blocked instruction pattern.",
            )

    return GuardDecision(
        allowed=True,
        reason="Request passed the prompt safety checks.",
    )
