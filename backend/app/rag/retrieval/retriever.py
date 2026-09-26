from typing import Any

from backend.app.rag.ingestion.document_loader import (
    chunk_document,
    load_document,
)


def build_local_index(
    file_path: str,
    *,
    chunk_size: int = 500,
    overlap: int = 75,
) -> list[dict[str, Any]]:
    """
    Build a deterministic local retrieval index from a document.
    """

    document = load_document(file_path)

    return chunk_document(
        document,
        chunk_size=chunk_size,
        overlap=overlap,
    )


def retrieve(
    chunks: list[dict[str, Any]],
    query: str,
    *,
    top_k: int = 3,
) -> list[dict[str, Any]]:
    """
    Retrieve chunks using simple lexical term matching.

    This is intentionally a deterministic baseline.
    Embedding-based semantic retrieval will replace/augment
    this layer later.
    """

    if not query.strip():
        return []

    query_terms = {
        term.lower().strip(".,:;!?()[]{}")
        for term in query.split()
        if term.strip()
    }

    scored: list[tuple[int, dict[str, Any]]] = []

    for chunk in chunks:
        text = chunk["text"].lower()

        score = sum(
            1
            for term in query_terms
            if term in text
        )

        if score > 0:
            scored.append((score, chunk))

    scored.sort(
        key=lambda item: (
            -item[0],
            item[1]["chunk_index"],
        )
    )

    return [
        chunk
        for _, chunk in scored[:top_k]
    ]
