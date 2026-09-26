import base64
import json
import subprocess
import urllib.error
import urllib.request
from typing import Any


PROJECT_ID = "project-1a1fb24e-7573-477f-871"
LOCATION = "us-central1"
MODEL = "gemini-2.5-flash"


def _get_access_token() -> str:
    return subprocess.check_output(
        ["gcloud", "auth", "print-access-token"],
        text=True,
    ).strip()


def analyze_image(
    image_bytes: bytes,
    prompt: str,
    mime_type: str = "image/png",
) -> str:
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    url = (
        f"https://{LOCATION}-aiplatform.googleapis.com/v1/"
        f"projects/{PROJECT_ID}/locations/{LOCATION}/"
        f"publishers/google/models/{MODEL}:generateContent"
    )

    payload: dict[str, Any] = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "inlineData": {
                            "mimeType": mime_type,
                            "data": image_b64,
                        }
                    },
                    {
                        "text": prompt,
                    },
                ],
            }
        ]
    }

    request = urllib.request.Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {_get_access_token()}",
            "Content-Type": "application/json",
            "x-goog-user-project": PROJECT_ID,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")

        raise RuntimeError(
            f"Vertex AI request failed: HTTP {exc.code}\n"
            f"{error_body}"
        ) from exc

    candidates = result.get("candidates", [])

    if not candidates:
        raise RuntimeError(
            "Vertex AI returned no candidates."
        )

    parts = candidates[0].get("content", {}).get("parts", [])

    text_parts = [
        part.get("text", "")
        for part in parts
        if part.get("text")
    ]

    if not text_parts:
        raise RuntimeError(
            "Vertex AI returned no text content."
        )

    return "\n".join(text_parts)
