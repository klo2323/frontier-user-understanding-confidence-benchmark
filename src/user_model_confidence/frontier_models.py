from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any


class FrontierModelError(RuntimeError):
    """Raised when a configured frontier provider cannot return a turn."""


DEFAULT_MODELS = {
    "openai": "gpt-4.1-mini",
    "anthropic": "claude-sonnet-4-5",
    "gemini": "gemini-2.5-flash",
}


SYSTEM_CONTEXT = (
    "You are participating in a research capture session. Respond normally to the user's request. "
    "Do not mention internal scoring, confidence traces, or evaluation machinery."
)


def call_frontier_model(
    *,
    provider: str,
    model: str | None,
    turns: list[dict[str, Any]],
    timeout: int = 60,
) -> dict[str, Any]:
    """Call a real configured frontier provider and return assistant text.

    This module intentionally has no mock-model fallback. If a provider key is missing,
    the caller gets a clear error instead of a fake assistant response.
    """

    normalized_provider = provider.strip().lower()
    normalized_model = (model or DEFAULT_MODELS.get(normalized_provider) or "").strip()
    if not normalized_model:
        raise FrontierModelError(f"No model configured for provider '{provider}'.")

    conversation = _conversation_after_first_user(turns)
    if not conversation:
        raise FrontierModelError("At least one user turn is required before calling a frontier model.")

    if normalized_provider == "openai":
        text = _call_openai(model=normalized_model, turns=conversation, timeout=timeout)
    elif normalized_provider == "anthropic":
        text = _call_anthropic(model=normalized_model, turns=conversation, timeout=timeout)
    elif normalized_provider == "gemini":
        text = _call_gemini(model=normalized_model, turns=conversation, timeout=timeout)
    else:
        raise FrontierModelError(f"Unsupported provider '{provider}'. Use openai, anthropic, or gemini.")

    return {
        "provider": normalized_provider,
        "model": normalized_model,
        "text": text.strip(),
    }


def _conversation_after_first_user(turns: list[dict[str, Any]]) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    seen_user = False
    for turn in turns:
        speaker = str(turn.get("speaker", "")).strip().lower()
        text = str(turn.get("text", "")).strip()
        if not text:
            continue
        if speaker not in {"user", "assistant"}:
            continue
        if speaker == "user":
            seen_user = True
        if not seen_user:
            continue
        normalized.append({"speaker": speaker, "text": text})
    return normalized


def _request_json(url: str, *, headers: dict[str, str], body: dict[str, Any], timeout: int) -> dict[str, Any]:
    encoded = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(url, data=encoded, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise FrontierModelError(f"Provider HTTP {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise FrontierModelError(f"Provider request failed: {error.reason}") from error


def _call_openai(*, model: str, turns: list[dict[str, str]], timeout: int) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise FrontierModelError("Set OPENAI_API_KEY to use the OpenAI router lane.")

    input_items: list[dict[str, str]] = [{"role": "system", "content": SYSTEM_CONTEXT}]
    for turn in turns:
        input_items.append({"role": turn["speaker"], "content": turn["text"]})

    data = _request_json(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        body={"model": model, "input": input_items},
        timeout=timeout,
    )

    output_text = data.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text

    chunks: list[str] = []
    for output in data.get("output", []) or []:
        for content in output.get("content", []) or []:
            text = content.get("text")
            if isinstance(text, str):
                chunks.append(text)
    if chunks:
        return "\n".join(chunks)
    raise FrontierModelError("OpenAI response did not include assistant text.")


def _call_anthropic(*, model: str, turns: list[dict[str, str]], timeout: int) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise FrontierModelError("Set ANTHROPIC_API_KEY to use the Anthropic router lane.")

    messages = [
        {"role": turn["speaker"], "content": turn["text"]}
        for turn in turns
        if turn["speaker"] in {"user", "assistant"}
    ]

    data = _request_json(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        },
        body={
            "model": model,
            "max_tokens": 900,
            "system": SYSTEM_CONTEXT,
            "messages": messages,
        },
        timeout=timeout,
    )

    chunks: list[str] = []
    for content in data.get("content", []) or []:
        if content.get("type") == "text" and isinstance(content.get("text"), str):
            chunks.append(content["text"])
    if chunks:
        return "\n".join(chunks)
    raise FrontierModelError("Anthropic response did not include assistant text.")


def _call_gemini(*, model: str, turns: list[dict[str, str]], timeout: int) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise FrontierModelError("Set GEMINI_API_KEY to use the Gemini router lane.")

    contents = []
    for turn in turns:
        role = "user" if turn["speaker"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": turn["text"]}]})

    data = _request_json(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}",
        headers={"Content-Type": "application/json"},
        body={
            "systemInstruction": {"parts": [{"text": SYSTEM_CONTEXT}]},
            "contents": contents,
        },
        timeout=timeout,
    )

    chunks: list[str] = []
    for candidate in data.get("candidates", []) or []:
        content = candidate.get("content") or {}
        for part in content.get("parts", []) or []:
            text = part.get("text")
            if isinstance(text, str):
                chunks.append(text)
    if chunks:
        return "\n".join(chunks)
    raise FrontierModelError("Gemini response did not include assistant text.")
