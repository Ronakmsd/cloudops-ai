from typing import Any


WORKSPACE_DEMO_DATA = [
    {
        "id": "doc-001",
        "title": "CloudOps Security Architecture",
        "type": "document",
        "owner": "cloudops-platform",
        "content": (
            "CloudOps AI uses defense-in-depth security, "
            "read-only database access, tool authorization, "
            "secure SQL validation, tenant isolation and "
            "confidential-data controls."
        ),
    },
    {
        "id": "doc-002",
        "title": "CloudOps Agent Deployment Guide",
        "type": "document",
        "owner": "cloudops-platform",
        "content": (
            "CloudOps agents should use authorized tools, "
            "ground responses in trusted enterprise knowledge, "
            "and record security-relevant tool execution events."
        ),
    },
]


def search_workspace(
    query: str,
    *,
    max_results: int = 5,
) -> dict[str, Any]:
    """
    Safe read-only Workspace-style enterprise search.

    This is a local demonstration connector, not a live
    Google Workspace integration.
    """
    if not query.strip():
        return {
            "success": False,
            "error": "Workspace search query cannot be empty.",
        }

    normalized_query = query.lower()

    matches = []

    for document in WORKSPACE_DEMO_DATA:
        searchable = (
            f"{document['title']} "
            f"{document['content']}"
        ).lower()

        if any(
            term in searchable
            for term in normalized_query.split()
            if len(term) > 2
        ):
            matches.append(
                {
                    "id": document["id"],
                    "title": document["title"],
                    "type": document["type"],
                    "owner": document["owner"],
                    "content": document["content"],
                    "source": "workspace_demo",
                }
            )

    return {
        "success": True,
        "query": query,
        "read_only": True,
        "source": "workspace_demo",
        "results": matches[:max_results],
    }
