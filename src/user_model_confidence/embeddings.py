from __future__ import annotations

import os
from typing import Any


DEFAULT_EMBEDDING_MODEL = "gemini-embedding-2"
DEFAULT_EMBEDDING_DIMENSIONS = 768


def check_embedding_health(
    *,
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: int = DEFAULT_EMBEDDING_DIMENSIONS,
) -> dict[str, Any]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {
            "status": "missing_api_key",
            "provider": "google",
            "model": model,
            "dimensions": dimensions,
            "ok": False,
            "message": "Set GEMINI_API_KEY in the backend environment.",
        }

    try:
        from google import genai
        from google.genai import types
    except ImportError as error:
        return {
            "status": "missing_dependency",
            "provider": "google",
            "model": model,
            "dimensions": dimensions,
            "ok": False,
            "message": f"Install google-genai to enable embeddings: {error}",
        }

    try:
        client = genai.Client(api_key=api_key)
        result = client.models.embed_content(
            model=model,
            contents="Embedding health check for user scoring engine.",
            config=types.EmbedContentConfig(output_dimensionality=dimensions),
        )
        values = result.embeddings[0].values
    except Exception as error:
        return {
            "status": "error",
            "provider": "google",
            "model": model,
            "dimensions": dimensions,
            "ok": False,
            "message": str(error),
        }

    return {
        "status": "ok",
        "provider": "google",
        "model": model,
        "dimensions": len(values),
        "ok": len(values) == dimensions,
        "message": "Gemini Embedding 2 is reachable from the backend.",
    }
