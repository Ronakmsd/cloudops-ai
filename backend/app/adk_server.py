from pathlib import Path
import os

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from google.adk.cli.fast_api import get_fast_api_app

from backend.app.agents.multimodal.gemini_multimodal import analyze_image


MAX_IMAGE_BYTES = 10 * 1024 * 1024


ALLOWED_IMAGE_TYPES = {
    "image/png",
    "image/jpeg",
    "image/webp",
}


def create_app() -> FastAPI:
    app = get_fast_api_app(
        agents_dir=str(Path(__file__).resolve().parent / "agents"),
        use_local_storage=False,
        web=False,
        allow_origins=[
            "regex:^(http://localhost:(5173|5174|8081)|https://cloudops-ai-frontend-944383402967[.]us-central1[.]run[.]app|https://cloudops-ai-frontend-xf6sboo7fa-uc[.]a[.]run[.]app)$"
        ],
        host="0.0.0.0",
        bind_host="0.0.0.0",
        port=int(os.environ.get("PORT", "8080")),
    )

    @app.post("/multimodal/analyze")
    async def multimodal_analyze(
        file: UploadFile = File(...),
        question: str = Form(...),
    ):
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=400,
                detail="Unsupported image type. Supported types: PNG, JPG, JPEG, WEBP.",
            )

        if not question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty.",
            )

        image_bytes = await file.read(MAX_IMAGE_BYTES + 1)

        if len(image_bytes) > MAX_IMAGE_BYTES:
            raise HTTPException(
                status_code=413,
                detail="Image exceeds the 10 MB upload limit.",
            )

        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty.",
            )

        try:
            analysis = analyze_image(
                image_bytes=image_bytes,
                prompt=question.strip(),
                mime_type=file.content_type,
            )
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Multimodal analysis failed: {exc}",
            ) from exc

        return {
            "success": True,
            "file_name": file.filename,
            "mime_type": file.content_type,
            "analysis": analysis,
        }

    return app


app = create_app()
