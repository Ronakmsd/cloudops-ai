from pathlib import Path
from typing import Any

from backend.app.agents.multimodal.gemini_multimodal import (
    analyze_image,
)


ALLOWED_IMAGE_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}


def analyze_local_image(
    image_path: str,
    question: str,
) -> dict[str, Any]:
    """
    Analyze a local image using Gemini multimodal inference.

    This tool is intended for trusted local application inputs.
    """

    path = Path(image_path)

    if not path.exists():
        return {
            "success": False,
            "error": "Image file does not exist.",
        }

    if not path.is_file():
        return {
            "success": False,
            "error": "Image path is not a file.",
        }

    mime_type = ALLOWED_IMAGE_TYPES.get(
        path.suffix.lower()
    )

    if mime_type is None:
        return {
            "success": False,
            "error": (
                "Unsupported image type. "
                "Supported types: PNG, JPG, JPEG, WEBP."
            ),
        }

    if not question.strip():
        return {
            "success": False,
            "error": "Question cannot be empty.",
        }

    try:
        result = analyze_image(
            image_bytes=path.read_bytes(),
            prompt=question,
            mime_type=mime_type,
        )

        return {
            "success": True,
            "file_name": path.name,
            "mime_type": mime_type,
            "analysis": result,
        }

    except Exception as exc:
        return {
            "success": False,
            "error": f"Multimodal analysis failed: {exc}",
        }
