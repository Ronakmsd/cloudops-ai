from dataclasses import dataclass


@dataclass(frozen=True)
class AuthorizationDecision:
    allowed: bool
    reason: str


ALLOWED_TOOLS = {
    "get_database_schema": {
        "action": "read_schema",
        "risk": "low",
    },
    "execute_read_only_sql": {
        "action": "read_database",
        "risk": "medium",
    },
    "search_workspace": {
        "action": "read_workspace",
        "risk": "low",
    },
}


def authorize_tool(
    tool_name: str,
    *,
    user_authorized: bool = True,
) -> AuthorizationDecision:
    """
    Authorize a CloudOps AI tool before execution.

    This is an additional policy layer and does not replace
    the underlying security controls implemented by each tool.
    """

    if not user_authorized:
        return AuthorizationDecision(
            allowed=False,
            reason="User is not authorized to use this tool.",
        )

    policy = ALLOWED_TOOLS.get(tool_name)

    if policy is None:
        return AuthorizationDecision(
            allowed=False,
            reason=f"Tool '{tool_name}' is not authorized.",
        )

    return AuthorizationDecision(
        allowed=True,
        reason=(
            f"Tool '{tool_name}' authorized for "
            f"{policy['action']} ({policy['risk']} risk)."
        ),
    )
