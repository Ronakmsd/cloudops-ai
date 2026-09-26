import logging
import os
import re
import time

from datetime import date, datetime
from decimal import Decimal
from typing import Any

import psycopg
from dotenv import load_dotenv

from backend.app.tools.audit import audit_sql_event
from backend.app.security.tool_authorization import authorize_tool

load_dotenv()

# Application DB role.
# This role is intentionally NOT SUPERUSER and NOT BYPASSRLS.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://cloudops_app:cloudops_app_dev_password@127.0.0.1:5432/cloudops",
)

MAX_ROWS = 100
MAX_QUERY_LENGTH = 5000
QUERY_TIMEOUT_MS = 5000

ALLOWED_TABLES = {
    "customers",
    "orders",
    "products",
}

FORBIDDEN_SCHEMA_PATTERNS = (
    r"\bpg_catalog\.",
    r"\bpg_toast\.",
    r"\binformation_schema\.",
    r"\bpg_user\b",
    r"\bpg_roles\b",
    r"\bpg_shadow\b",
    r"\bpg_authid\b",
)

TENANT_SCOPED_TABLES = {
    "customers",
    "orders",
    "products",
}

logger = logging.getLogger("cloudops.sql")


class SQLSecurityError(Exception):
    """Raised when a SQL request violates the read-only policy."""


def _json_safe(value: Any) -> Any:
    """Convert PostgreSQL/Python values into JSON-compatible values."""
    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    if isinstance(value, (str, int, float, bool)) or value is None:
        return value

    return str(value)


def _validate_select_query(query: str) -> str:
    query = query.strip()

    if not query:
        raise SQLSecurityError("SQL query cannot be empty.")

    if len(query) > MAX_QUERY_LENGTH:
        raise SQLSecurityError(
            f"SQL query exceeds the maximum allowed length "
            f"of {MAX_QUERY_LENGTH} characters."
        )

    if ";" in query.rstrip(";"):
        raise SQLSecurityError(
            "Multiple SQL statements are not allowed."
        )

    query = query.rstrip(";").strip()

    if not re.match(
        r"^(SELECT|WITH)\b",
        query,
        re.IGNORECASE,
    ):
        raise SQLSecurityError(
            "Only read-only SELECT or WITH queries are allowed."
        )

    forbidden = re.compile(
        r"\b("
        r"INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|"
        r"CREATE|GRANT|REVOKE|MERGE|CALL|COPY"
        r")\b",
        re.IGNORECASE,
    )

    if forbidden.search(query):
        raise SQLSecurityError(
            "Query contains a prohibited SQL operation."
        )

    if "--" in query or "/*" in query or "*/" in query:
        raise SQLSecurityError(
            "SQL comments are not allowed."
        )

    for pattern in FORBIDDEN_SCHEMA_PATTERNS:
        if re.search(
            pattern,
            query,
            re.IGNORECASE,
        ):
            raise SQLSecurityError(
                "Access to system schemas or database metadata "
                "is not allowed."
            )

    table_references = re.findall(
        r"\b(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)",
        query,
        re.IGNORECASE,
    )

    for table in table_references:
        if table.lower() not in ALLOWED_TABLES:
            raise SQLSecurityError(
                f"Access to table '{table}' is not allowed."
            )

    return query


def _validate_tenant_context(
    query: str,
    tenant_id: str | None,
) -> None:
    """
    Validate that tenant-scoped database access has an
    application-authorized tenant context.

    PostgreSQL RLS remains the authoritative row-level
    enforcement boundary.
    """

    if tenant_id is None:
        raise SQLSecurityError(
            "Tenant ID is required for database access."
        )

    tenant_id = tenant_id.strip()

    if not tenant_id:
        raise SQLSecurityError(
            "Tenant ID cannot be empty."
        )

    table_references = re.findall(
        r"\b(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)",
        query,
        re.IGNORECASE,
    )

    referenced_tenant_tables = {
        table.lower()
        for table in table_references
        if table.lower() in TENANT_SCOPED_TABLES
    }

    if referenced_tenant_tables and not tenant_id:
        raise SQLSecurityError(
            "Tenant context is required for tenant-scoped tables."
        )


def execute_read_only_sql(
    query: str,
    *,
    tenant_id: str | None = None,
) -> dict[str, Any]:
    """
    Execute a validated read-only SQL query against PostgreSQL.

    The application database role is intentionally restricted
    from bypassing PostgreSQL Row-Level Security.

    tenant_id is supplied by the server-side SecurityContext,
    never by the LLM.
    """

    start = time.perf_counter()

    authorization = authorize_tool(
        "execute_read_only_sql",
        user_authorized=True,
    )

    if not authorization.allowed:
        duration_ms = (
            time.perf_counter() - start
        ) * 1000

        audit_sql_event(
            query=query,
            success=False,
            status="unauthorized",
            duration_ms=duration_ms,
            error=authorization.reason,
        )

        raise SQLSecurityError(
            authorization.reason
        )

    try:
        query = _validate_select_query(query)

        _validate_tenant_context(
            query,
            tenant_id,
        )

    except SQLSecurityError as exc:
        duration_ms = (
            time.perf_counter() - start
        ) * 1000

        audit_sql_event(
            query=query,
            success=False,
            status="blocked",
            duration_ms=duration_ms,
            error=str(exc),
        )

        raise

    try:
        with psycopg.connect(
            DATABASE_URL,
            options=f"-c statement_timeout={QUERY_TIMEOUT_MS}",
        ) as conn:

            with conn.cursor() as cursor:

                # Set PostgreSQL transaction-local tenant context.
                #
                # IMPORTANT:
                # tenant_id comes from the server-side SecurityContext.
                # It is NOT supplied by the LLM.
                cursor.execute(
                    "SELECT set_config(%s, %s, true)",
                    (
                        "app.tenant_id",
                        tenant_id,
                    ),
                )

                cursor.execute(query)

                columns = [
                    description.name
                    for description in cursor.description
                ]

                rows = cursor.fetchmany(MAX_ROWS)

                result = {
                    "success": True,
                    "columns": columns,
                    "rows": [
                        [
                            _json_safe(value)
                            for value in row
                        ]
                        for row in rows
                    ],
                    "row_count": len(rows),
                    "max_rows": MAX_ROWS,
                    "tenant_context": tenant_id,
                }

        duration_ms = (
            time.perf_counter() - start
        ) * 1000

        audit_sql_event(
            query=query,
            success=True,
            status="success",
            row_count=len(rows),
            duration_ms=duration_ms,
        )

        return result

    except Exception as exc:
        duration_ms = (
            time.perf_counter() - start
        ) * 1000

        audit_sql_event(
            query=query,
            success=False,
            status="database_error",
            duration_ms=duration_ms,
            error=type(exc).__name__,
        )

        raise
