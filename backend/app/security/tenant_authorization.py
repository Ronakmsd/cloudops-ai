from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityContext:
    user_id: str
    tenant_id: str
    role: str


@dataclass(frozen=True)
class TenantAuthorizationDecision:
    allowed: bool
    reason: str


ROLE_PERMISSIONS = {
    "viewer": {
        "get_database_schema",
        "execute_read_only_sql",
        "search_workspace",
    },
    "analyst": {
        "get_database_schema",
        "execute_read_only_sql",
        "search_workspace",
    },
    "admin": {
        "get_database_schema",
        "execute_read_only_sql",
        "search_workspace",
    },
}


def authorize_tenant_tool(
    context: SecurityContext,
    *,
    target_tenant_id: str,
    tool_name: str,
) -> TenantAuthorizationDecision:

    if context.tenant_id != target_tenant_id:
        return TenantAuthorizationDecision(
            False,
            "Cross-tenant access is not authorized.",
        )

    permissions = ROLE_PERMISSIONS.get(context.role)

    if permissions is None:
        return TenantAuthorizationDecision(
            False,
            f"Unknown role '{context.role}'.",
        )

    if tool_name not in permissions:
        return TenantAuthorizationDecision(
            False,
            f"Role '{context.role}' is not authorized for tool '{tool_name}'.",
        )

    return TenantAuthorizationDecision(
        True,
        (
            f"Tenant '{context.tenant_id}' authorized "
            f"for role '{context.role}' and tool '{tool_name}'."
        ),
    )
