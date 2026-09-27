from typing import Any

from google.adk.tools.tool_context import ToolContext

from backend.app.security.identity import get_security_context
from backend.app.tools.tenant_data import create_tenant_sql_tool


def tenant_guarded_execute_sql(
    query: str,
    user_request: str,
    tool_context: ToolContext,
) -> dict[str, Any]:
    """
    Execute read-only SQL using a server-side SecurityContext
    resolved from the current ADK request user.

    The LLM can provide SQL, but it cannot choose the tenant.
    Tenant identity comes from the server-side identity mapping.
    """

    security_context = get_security_context(tool_context.user_id)

    tenant_sql_tool = create_tenant_sql_tool(security_context)

    return tenant_sql_tool(
        query,
        user_request=user_request,
        user_authorized=True,
    )
