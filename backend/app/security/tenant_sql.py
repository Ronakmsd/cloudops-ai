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

    import re

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

    if not tenant_tables:
        return TenantSQLDecision(
            True,
            "Query does not reference a tenant-scoped table.",
        )

    # Tenant-aware execution must explicitly identify the
    # tenant column in queries touching tenant-scoped tables.
    if "tenant_id" not in normalized:
        return TenantSQLDecision(
            False,
            (
                "Tenant-scoped query must explicitly include "
                "tenant_id filtering."
            ),
        )

    return TenantSQLDecision(
        True,
        (
            f"Tenant-scoped SQL accepted for tenant "
            f"'{tenant_id}'."
        ),
    )
