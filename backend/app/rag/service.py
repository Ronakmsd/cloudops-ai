from pathlib import Path
from typing import Any

from backend.app.rag.embeddings.gemini_embeddings import (
    embed_text,
    embed_texts,
)
from backend.app.rag.ingestion.document_loader import (
    chunk_document,
    load_document,
)
from backend.app.rag.ingestion.pdf_to_document import (
    load_pdf_as_document,
    load_and_chunk_pdf,
)


from backend.app.rag.retrieval.vector_store import (
    LocalVectorStore,
)


class RAGService:
    """
    Enterprise document retrieval service.

    Handles document ingestion, chunking, embedding,
    indexing and semantic retrieval.
    """

    def __init__(
        self,
        *,
        chunk_size: int = 500,
        overlap: int = 75,
    ) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.vector_store = LocalVectorStore()

        self.documents: dict[str, dict[str, Any]] = {}

    def ingest_document(
        self,
        file_path: str,
    ) -> dict[str, Any]:
        """
        Load, chunk and index a document.
        """

        suffix = Path(file_path).suffix.lower()

        if suffix == ".pdf":
            document = load_pdf_as_document(file_path)
            chunks = load_and_chunk_pdf(
                file_path,
                chunk_size=self.chunk_size,
                overlap=self.overlap,
            )
        else:
            document = load_document(file_path)
            chunks = chunk_document(
                document,
                chunk_size=self.chunk_size,
                overlap=self.overlap,
            )

        embeddings = embed_texts(
            [chunk["text"] for chunk in chunks]
        )

        for chunk, embedding in zip(
            chunks,
            embeddings,
        ):
            self.vector_store.add(
                chunk=chunk,
                embedding=embedding,
            )

        self.documents[
            document["document_id"]
        ] = {
            "file_name": document["file_name"],
            "file_type": document["file_type"],
            "chunk_count": len(chunks),
        }

        return {
            "document_id": document["document_id"],
            "file_name": document["file_name"],
            "chunk_count": len(chunks),
        }

    def retrieve(
        self,
        query: str,
        *,
        top_k: int = 3,
    ) -> list[dict[str, Any]]:
        """
        Perform semantic retrieval for a natural-language query.
        """

        query_embedding = embed_text(query)

        return self.vector_store.search(
            query_embedding,
            top_k=top_k,
        )

    def get_context(
        self,
        query: str,
        *,
        top_k: int = 3,
    ) -> str:
        """
        Return retrieved chunks as grounded context.
        """

        results = self.retrieve(
            query,
            top_k=top_k,
        )

        if not results:
            return ""

        context_parts = []

        for result in results:
            chunk = result["chunk"]

            source = chunk["document_id"]
            chunk_id = chunk["chunk_id"]

            if chunk.get("source_type") == "pdf":
                source = chunk.get(
                    "file_name",
                    source,
                )
                page_number = chunk.get(
                    "page_number",
                    "unknown",
                )

                context_parts.append(
                    (
                        f"[Source: {source} | "
                        f"Page: {page_number} | "
                        f"Chunk: {chunk_id}]\n"
                        f"{chunk['text']}"
                    )
                )
            else:
                context_parts.append(
                    (
                        f"[Source: {source} | "
                        f"Chunk: {chunk_id}]\n"
                        f"{chunk['text']}"
                    )
                )

        return "\n\n".join(context_parts)

    @property
    def document_count(self) -> int:
        return len(self.documents)

    @property
    def chunk_count(self) -> int:
        return self.vector_store.size
