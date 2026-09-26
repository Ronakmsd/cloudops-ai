import json
import logging
import time
from typing import Any


logger = logging.getLogger("cloudops.audit")


def audit_sql_event(
    *,
    query: str,
    success: bool,
    status: str,
    row_count: int = 0,
    duration_ms: float = 0.0,
    error: str | None = None,
) -> None:
    """
    Record security-relevant SQL execution metadata.

    Never log returned database rows or sensitive query results.
    """

    event: dict[str, Any] = {
        "event": "sql_tool_execution",
        "success": success,
        "status": status,
        "query_length": len(query),
        "row_count": row_count,
        "duration_ms": round(duration_ms, 2),
    }

    if error:
        event["error"] = error

    logger.info(json.dumps(event, sort_keys=True))
