from typing import Any

from backend.app.rag.ingestion.pdf_loader import load_pdf


def load_pdf_as_document(file_path: str) -> dict[str, Any]:
    """
    Load a PDF and normalize it into the CloudOps AI
    document structure while preserving page information.
    """
    result = load_pdf(file_path)

    return {
        "document_id": result["document_id"],
        "file_name": result["file_name"],
        "file_type": result["file_type"],
        "page_count": result["page_count"],
        "character_count": result["character_count"],
        "text": result["text"],
        "content": result["text"],
        "pages": result["pages"],
    }


def load_and_chunk_pdf(
    file_path: str,
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[dict[str, Any]]:
    """
    Load a PDF and create page-aware RAG chunks.

    Each chunk retains the PDF page number that contains
    the chunk text.
    """
    document = load_pdf_as_document(file_path)

    chunks: list[dict[str, Any]] = []
    chunk_index = 0

    for page in document["pages"]:
        page_number = page["page_number"]
        page_text = page["text"].strip()

        if not page_text:
            continue

        page_document = {
            "document_id": document["document_id"],
            "file_name": document["file_name"],
            "file_type": document["file_type"],
            "content": page_text,
        }

        from backend.app.rag.ingestion.document_loader import chunk_document

        page_chunks = chunk_document(
            page_document,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        for chunk in page_chunks:
            chunk["source_type"] = "pdf"
            chunk["file_name"] = document["file_name"]
            chunk["page_number"] = page_number
            chunk["page_count"] = document["page_count"]

            # Keep globally unique chunk IDs across PDF pages.
            chunk["chunk_id"] = (
                f"{document['document_id']}_"
                f"page_{page_number}_"
                f"{chunk_index}"
            )
            chunk["chunk_index"] = chunk_index

            chunks.append(chunk)
            chunk_index += 1

    return chunks
