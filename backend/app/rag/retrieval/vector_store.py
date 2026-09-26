import math
from typing import Any


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    """Calculate cosine similarity between two vectors."""

    if not vector_a or not vector_b:
        raise ValueError("Vectors cannot be empty.")

    if len(vector_a) != len(vector_b):
        raise ValueError(
            "Vectors must have the same dimensions."
        )

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (
        magnitude_a * magnitude_b
    )


class LocalVectorStore:
    """Simple in-memory vector store for RAG development."""

    def __init__(self) -> None:
        self._records: list[dict[str, Any]] = []

    def add(
        self,
        *,
        chunk: dict[str, Any],
        embedding: list[float],
    ) -> None:
        self._records.append(
            {
                "chunk": chunk,
                "embedding": embedding,
            }
        )

    def search(
        self,
        query_embedding: list[float],
        *,
        top_k: int = 3,
    ) -> list[dict[str, Any]]:
        if not self._records:
            return []

        scored = []

        for record in self._records:
            score = cosine_similarity(
                query_embedding,
                record["embedding"],
            )

            scored.append(
                {
                    "chunk": record["chunk"],
                    "score": score,
                }
            )

        scored.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return scored[:top_k]

    @property
    def size(self) -> int:
        return len(self._records)
