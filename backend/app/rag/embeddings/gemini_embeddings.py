import os
from typing import Any

from dotenv import load_dotenv
from google import genai

load_dotenv()


PROJECT_ID = os.getenv(
    "GOOGLE_CLOUD_PROJECT",
    "project-1a1fb24e-7573-477f-871",
)

LOCATION = os.getenv(
    "GOOGLE_CLOUD_LOCATION",
    "us-central1",
)

EMBEDDING_MODEL = "text-embedding-004"


client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
)


def embed_text(text: str) -> list[float]:
    """
    Generate a semantic embedding for a single text input.
    """

    if not text.strip():
        raise ValueError("Text cannot be empty.")

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=[text],
    )

    if not response.embeddings:
        raise RuntimeError(
            "Embedding API returned no embeddings."
        )

    values = response.embeddings[0].values

    if values is None:
        raise RuntimeError(
            "Embedding API returned an empty vector."
        )

    return list(values)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Generate semantic embeddings for multiple text inputs.
    """

    if not texts:
        return []

    if any(not text.strip() for text in texts):
        raise ValueError(
            "Embedding inputs cannot contain empty text."
        )

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts,
    )

    if not response.embeddings:
        raise RuntimeError(
            "Embedding API returned no embeddings."
        )

    return [
        list(embedding.values)
        for embedding in response.embeddings
    ]
