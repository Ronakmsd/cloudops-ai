from typing import Any

from backend.app.security.prompt_guard import check_prompt_safety
from backend.app.security.tool_authorization import authorize_tool
from backend.app.security.tenant_authorization import (
    SecurityContext,
    authorize_tenant_tool,
)
from backend.app.security.tenant_sql import validate_tenant_sql
from backend.app.tools.secure_sql import execute_read_only_sql


def guarded_execute_sql(
    query: str,
    *,
    user_request: str,
    user_authorized: bool = True,
    security_context: SecurityContext | None = None,
    target_tenant_id: str | None = None,
) -> dict[str, Any]:

    prompt_decision = check_prompt_safety(user_request)

    if not prompt_decision.allowed:
        raise PermissionError(
            f"Prompt blocked: {prompt_decision.reason}"
        )

    authorization = authorize_tool(
        "execute_read_only_sql",
        user_authorized=user_authorized,
    )

    if not authorization.allowed:
        raise PermissionError(
            f"Tool authorization denied: {authorization.reason}"
        )

    if security_context is not None:
        if target_tenant_id is None:
            raise PermissionError(
                "Target tenant is required for tenant-aware SQL access."
            )

        tenant_decision = authorize_tenant_tool(
            security_context,
            target_tenant_id=target_tenant_id,
            tool_name="execute_read_only_sql",
        )

        if not tenant_decision.allowed:
            raise PermissionError(
                tenant_decision.reason
            )

        tenant_sql_decision = validate_tenant_sql(
            query,
            tenant_id=security_context.tenant_id,
        )

        if not tenant_sql_decision.allowed:
            raise PermissionError(
                tenant_sql_decision.reason
            )

        if security_context.tenant_id != target_tenant_id:
            raise PermissionError(
                "Security context tenant does not match target tenant."
            )

    return execute_read_only_sql(
        query,
        tenant_id=(
            security_context.tenant_id
            if security_context is not None
            else None
        ),
    )
