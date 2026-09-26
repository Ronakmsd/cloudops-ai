from typing import Any

from backend.app.security.prompt_guard import check_prompt_safety
from backend.app.security.tool_authorization import authorize_tool
from backend.app.security.tenant_authorization import (
    SecurityContext,
    authorize_tenant_tool,
)
from backend.app.tools.workspace.workspace_search import search_workspace


def guarded_workspace_search(
    query: str,
    *,
    user_request: str,
    user_authorized: bool = True,
    security_context: SecurityContext | None = None,
    target_tenant_id: str | None = None,
    max_results: int = 5,
) -> dict[str, Any]:

    prompt_decision = check_prompt_safety(user_request)

    if not prompt_decision.allowed:
        raise PermissionError(prompt_decision.reason)

    authorization = authorize_tool(
        "search_workspace",
        user_authorized=user_authorized,
    )

    if not authorization.allowed:
        raise PermissionError(authorization.reason)

    if security_context is not None:
        if target_tenant_id is None:
            raise PermissionError(
                "Target tenant is required for tenant-aware access."
            )

        tenant_decision = authorize_tenant_tool(
            security_context,
            target_tenant_id=target_tenant_id,
            tool_name="search_workspace",
        )

        if not tenant_decision.allowed:
            raise PermissionError(tenant_decision.reason)

    return search_workspace(
        query,
        max_results=max_results,
    )
