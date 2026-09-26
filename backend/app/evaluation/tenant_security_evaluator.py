from typing import Any

from backend.app.security.tenant_authorization import SecurityContext
from backend.app.tools.tenant_data import create_tenant_sql_tool


def run_tenant_security_evaluation() -> dict[str, Any]:
    context = SecurityContext(
        user_id="security-test-user",
        tenant_id="tenant-a",
        role="viewer",
    )

    tool = create_tenant_sql_tool(context)

    results: list[dict[str, Any]] = []

    # 1. Authorized tenant access
    authorized = tool(
        """
        SELECT customer_id, customer_name, tenant_id
        FROM customers
        ORDER BY customer_id
        """,
        user_request="List my customers.",
    )

    authorized_rows = authorized["rows"]

    results.append({
        "test": "authorized_tenant_access",
        "passed": (
            authorized["success"]
            and len(authorized_rows) == 2
            and all(
                row[2] == "tenant-a"
                for row in authorized_rows
            )
        ),
    })

    # 2. Explicit cross-tenant SQL
    cross_tenant = tool(
        """
        SELECT customer_id, customer_name, tenant_id
        FROM customers
        WHERE tenant_id = 'tenant-b'
        ORDER BY customer_id
        """,
        user_request="Retrieve tenant-b customers.",
    )

    results.append({
        "test": "cross_tenant_sql_blocked_by_rls",
        "passed": (
            cross_tenant["success"]
            and len(cross_tenant["rows"]) == 0
        ),
    })

    # 3. Another tenant's data through a different table
    cross_tenant_orders = tool(
        """
        SELECT order_id, customer_id, tenant_id
        FROM orders
        WHERE tenant_id = 'tenant-b'
        ORDER BY order_id
        """,
        user_request="Retrieve tenant-b orders.",
    )

    results.append({
        "test": "cross_tenant_orders_blocked",
        "passed": (
            cross_tenant_orders["success"]
            and len(cross_tenant_orders["rows"]) == 0
        ),
    })

    # 4. Another tenant's products
    cross_tenant_products = tool(
        """
        SELECT product_id, product_name, tenant_id
        FROM products
        WHERE tenant_id = 'tenant-b'
        ORDER BY product_id
        """,
        user_request="Retrieve tenant-b products.",
    )

    results.append({
        "test": "cross_tenant_products_blocked",
        "passed": (
            cross_tenant_products["success"]
            and len(cross_tenant_products["rows"]) == 0
        ),
    })

    # 5. Destructive SQL
    destructive_blocked = False

    try:
        tool(
            "DELETE FROM customers",
            user_request="Delete all customers.",
        )
    except Exception:
        destructive_blocked = True

    results.append({
        "test": "destructive_sql_blocked",
        "passed": destructive_blocked,
    })

    # 6. System schema access
    system_schema_blocked = False

    try:
        tool(
            """
            SELECT rolname
            FROM pg_roles
            """,
            user_request="Show database roles.",
        )
    except Exception:
        system_schema_blocked = True

    results.append({
        "test": "system_schema_access_blocked",
        "passed": system_schema_blocked,
    })

    # 7. SQL comments
    comments_blocked = False

    try:
        tool(
            """
            SELECT customer_id
            FROM customers
            -- bypass attempt
            """,
            user_request="List customer IDs.",
        )
    except Exception:
        comments_blocked = True

    results.append({
        "test": "sql_comments_blocked",
        "passed": comments_blocked,
    })

    # 8. Multiple statements
    multi_statement_blocked = False

    try:
        tool(
            """
            SELECT customer_id FROM customers;
            SELECT customer_id FROM customers;
            """,
            user_request="Run database queries.",
        )
    except Exception:
        multi_statement_blocked = True

    results.append({
        "test": "multiple_statements_blocked",
        "passed": multi_statement_blocked,
    })

    # 9. Unknown table
    unknown_table_blocked = False

    try:
        tool(
            """
            SELECT *
            FROM secret_internal_table
            """,
            user_request="Inspect internal data.",
        )
    except Exception:
        unknown_table_blocked = True

    results.append({
        "test": "unknown_table_blocked",
        "passed": unknown_table_blocked,
    })

    # 10. Tenant identity cannot be changed by tool caller
    tenant_override_blocked = False

    try:
        from backend.app.tools.guarded_sql import guarded_execute_sql

        guarded_execute_sql(
            """
            SELECT customer_id, customer_name, tenant_id
            FROM customers
            WHERE tenant_id = 'tenant-b'
            """,
            user_request="Retrieve tenant-b customers.",
            security_context=context,
            target_tenant_id="tenant-b",
        )
    except Exception:
        tenant_override_blocked = True

    results.append({
        "test": "tenant_identity_override_blocked",
        "passed": tenant_override_blocked,
    })

    passed = sum(
        1
        for result in results
        if result["passed"]
    )

    return {
        "suite": "CloudOps AI Tenant Security Evaluation",
        "total_tests": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "score": (
            passed / len(results)
            if results
            else 0.0
        ),
        "results": results,
    }


if __name__ == "__main__":
    evaluation = run_tenant_security_evaluation()

    print("=" * 50)
    print("CLOUDOPS AI TENANT SECURITY EVALUATION")
    print("=" * 50)

    for result in evaluation["results"]:
        status = "PASS" if result["passed"] else "FAIL"
        print(
            f"{status:<6} "
            f"{result['test']}"
        )

    print("=" * 50)
    print(
        f"{evaluation['passed']}/"
        f"{evaluation['total_tests']} TESTS PASSED"
    )

    print(
        f"SCORE: "
        f"{evaluation['score']:.2f}"
    )

    print("=" * 50)

    if evaluation["failed"]:
        raise SystemExit(1)
