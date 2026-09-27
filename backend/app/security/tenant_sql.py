import re
from dataclasses import dataclass


@dataclass(frozen=True)
class TenantSQLDecision:
    allowed: bool
    reason: str


TENANT_SCOPED_TABLES = {
    "customers",
    "products",
    "orders",
}


def validate_tenant_sql(
    query: str,
    *,
    tenant_id: str,
) -> TenantSQLDecision:
    normalized = query.strip().lower()

    if not tenant_id.strip():
        return TenantSQLDecision(
            False,
            "Tenant ID is required for tenant-scoped SQL.",
        )

    referenced_tables: set[str] = set()

    matches = re.findall(
        r"\b(?:from|join)\s+([a-zA-Z_][a-zA-Z0-9_]*)",
        normalized,
        re.IGNORECASE,
    )

    for table in matches:
        referenced_tables.add(table.lower())

    tenant_tables = referenced_tables.intersection(
        TENANT_SCOPED_TABLES
    )

    # Query does not touch tenant-scoped tables.
    if not tenant_tables:
        return TenantSQLDecision(
            True,
            "Query does not reference a tenant-scoped table.",
        )

    # Every tenant-scoped query must explicitly reference tenant_id.
    if "tenant_id" not in normalized:
        return TenantSQLDecision(
            False,
            "Tenant-scoped query must explicitly include tenant_id filtering.",
        )

    # Conservative defense-in-depth:
    # Do not allow OR in tenant-scoped queries.
    # OR can weaken or bypass a simple tenant predicate.
    if re.search(r"\bOR\b", normalized, re.IGNORECASE):
        return TenantSQLDecision(
            False,
            (
                "Tenant-scoped SQL cannot use OR because it may "
                "weaken tenant isolation."
            ),
        )

    # Do not allow UNION in tenant-scoped queries.
    # Every UNION branch would otherwise need independent
    # tenant-isolation validation.
    if re.search(r"\bUNION\b", normalized, re.IGNORECASE):
        return TenantSQLDecision(
            False,
            (
                "UNION is not allowed in tenant-scoped SQL "
                "because every result branch must independently "
                "satisfy tenant isolation."
            ),
        )

    # Tenant identity MUST come from the server-controlled
    # PostgreSQL setting. Literal tenant IDs are forbidden.
    required_predicate = (
        "tenant_id = current_setting('app.tenant_id', true)"
    )

    if required_predicate not in normalized:
        return TenantSQLDecision(
            False,
            (
                "Tenant-scoped SQL must use the server-controlled "
                "app.tenant_id setting. Literal tenant IDs are not allowed."
            ),
        )

    return TenantSQLDecision(
        True,
        (
            "Tenant-scoped SQL accepted for server-authorized "
            f"tenant '{tenant_id}'."
        ),
    )
