from pathlib import Path
from typing import Any

from pypdf import PdfReader


def load_pdf(file_path: str) -> dict[str, Any]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"PDF not found: {file_path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Path is not a file: {file_path}"
        )

    if path.suffix.lower() != ".pdf":
        raise ValueError(
            "Expected a PDF file."
        )

    reader = PdfReader(str(path))

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1,
    ):
        text = page.extract_text() or ""

        pages.append(
            {
                "page_number": page_number,
                "text": text,
                "character_count": len(text),
            }
        )

    full_text = "\n\n".join(
        page["text"]
        for page in pages
    )

    return {
        "document_id": path.stem,
        "file_name": path.name,
        "file_type": "application/pdf",
        "page_count": len(pages),
        "character_count": len(full_text),
        "text": full_text,
        "pages": pages,
    }
