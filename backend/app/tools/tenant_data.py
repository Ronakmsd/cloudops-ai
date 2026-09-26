from typing import Any

from backend.app.security.tenant_authorization import (
    SecurityContext,
)
from backend.app.tools.guarded_sql import guarded_execute_sql


def create_tenant_sql_tool(
    security_context: SecurityContext,
):
    """
    Create a SQL tool permanently bound to the supplied
    server-side security context.

    The agent can provide SQL, but cannot choose or change
    the tenant identity.
    """

    tenant_id = security_context.tenant_id

    def tenant_guarded_execute_sql(
        query: str,
        *,
        user_request: str,
        user_authorized: bool = True,
    ) -> dict[str, Any]:
        return guarded_execute_sql(
            query,
            user_request=user_request,
            user_authorized=user_authorized,
            security_context=security_context,
            target_tenant_id=tenant_id,
        )

    tenant_guarded_execute_sql.__name__ = (
        "tenant_guarded_execute_sql"
    )

    tenant_guarded_execute_sql.__doc__ = (
        f"Execute read-only SQL for the authorized tenant "
        f"context. Tenant identity is fixed by the application "
        f"and cannot be selected by the agent."
    )

    return tenant_guarded_execute_sql
