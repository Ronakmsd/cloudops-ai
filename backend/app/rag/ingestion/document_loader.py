from pathlib import Path
from typing import Any


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
}


def load_document(file_path: str) -> dict[str, Any]:
    """
    Load a supported text-based enterprise document.

    Returns normalized document metadata and content.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported document type: {path.suffix}"
        )

    content = path.read_text(
        encoding="utf-8",
        errors="replace",
    ).strip()

    if not content:
        raise ValueError(
            "Document is empty."
        )

    return {
        "document_id": path.stem,
        "file_name": path.name,
        "file_type": path.suffix.lower(),
        "content": content,
        "character_count": len(content),
    }


def chunk_document(
    document: dict[str, Any],
    *,
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[dict[str, Any]]:
    """
    Split a document into overlapping text chunks.

    Overlap preserves local context between neighboring chunks.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be >= 0 and smaller than chunk_size."
        )

    content = document["content"]

    chunks: list[dict[str, Any]] = []

    start = 0
    chunk_index = 0

    while start < len(content):
        end = min(
            start + chunk_size,
            len(content),
        )

        chunk_text = content[start:end].strip()

        if chunk_text:
            chunks.append(
                {
                    "document_id": document["document_id"],
                    "chunk_id": f"{document['document_id']}_{chunk_index}",
                    "chunk_index": chunk_index,
                    "text": chunk_text,
                    "start_char": start,
                    "end_char": end,
                }
            )

        if end >= len(content):
            break

        start = end - overlap
        chunk_index += 1

    return chunks
