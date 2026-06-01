from __future__ import annotations

import argparse
import json
import mimetypes
import re
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from user_model_confidence.embeddings import check_embedding_health
from user_model_confidence.frontier_models import FrontierModelError, call_frontier_model
from user_model_confidence.scorer import score_conversation


REPO_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_ROOT = REPO_ROOT / "frontend"
NATIVE_CAPTURE_ROOT = REPO_ROOT / "data" / "native_capture"
ROUTER_RUN_ROOT = REPO_ROOT / "data" / "router_runs"


class FrontendHandler(BaseHTTPRequestHandler):
    server_version = "UserModelConfidenceFrontend/0.2"

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self) -> None:
        if self.path in {"/", "/index.html"}:
            self.respond_file(FRONTEND_ROOT / "index.html")
            return
        if self.path in {"/app.js", "/styles.css"}:
            self.respond_file(FRONTEND_ROOT / self.path.lstrip("/"))
            return
        if self.path == "/health":
            self.respond_json({"status": "ok"}, status=200)
            return
        if self.path == "/embedding-health":
            result = check_embedding_health()
            self.respond_json(result, status=200 if result["ok"] else 503)
            return
        if self.path == "/native-captures":
            self.respond_json({"captures": list_native_captures()}, status=200)
            return
        if self.path == "/router-runs":
            self.respond_json({"runs": list_router_runs()}, status=200)
            return
        self.respond_json({"error": "Not found."}, status=404)

    def do_POST(self) -> None:
        if self.path == "/score-conversation":
            self.handle_score_conversation()
            return
        if self.path == "/frontier-turn":
            self.handle_frontier_turn()
            return
        if self.path == "/native-capture":
            self.handle_native_capture()
            return
        self.respond_json({"error": "Not found."}, status=404)

    def handle_score_conversation(self) -> None:
        try:
            payload = self.read_json_body()
            result = score_conversation(payload)
        except Exception as error:
            self.respond_json({"error": str(error)}, status=400)
            return
        self.respond_json(result, status=200)

    def handle_frontier_turn(self) -> None:
        try:
            payload = self.read_json_body()
            turns = payload.get("turns")
            if not isinstance(turns, list):
                raise ValueError("turns must be an array.")
            model_response = call_frontier_model(
                provider=str(payload.get("model_provider", "")),
                model=str(payload.get("model_name", "")),
                turns=turns,
            )
            assistant_turn = {
                "turn_id": f"t{len(turns) + 1}",
                "speaker": "assistant",
                "text": model_response["text"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            updated_turns = [*turns, assistant_turn]
            score_request = {
                "conversation_id": str(payload.get("conversation_id") or "router-capture"),
                "user_id": str(payload.get("user_id") or "router-user"),
                "turns": updated_turns,
                "conversation_metadata": {
                    **payload.get("conversation_metadata", {}),
                    "capture_lane": "controlled_frontier_router",
                    "model_provider": model_response["provider"],
                    "model_name": model_response["model"],
                },
            }
            if "ground_truth_labels" in payload:
                score_request["ground_truth_labels"] = payload["ground_truth_labels"]
            result = score_conversation(score_request)
            saved_path = save_router_run(
                score_request["conversation_id"],
                score_request,
                {
                    "model_provider": model_response["provider"],
                    "model_name": model_response["model"],
                    "assistant_turn": assistant_turn,
                    "turns": updated_turns,
                    "score_result": result,
                },
            )
        except FrontierModelError as error:
            self.respond_json({"error": str(error), "error_type": "frontier_model"}, status=400)
            return
        except Exception as error:
            self.respond_json({"error": str(error)}, status=400)
            return

        self.respond_json(
            {
                "conversation_id": payload.get("conversation_id"),
                "model_provider": model_response["provider"],
                "model_name": model_response["model"],
                "assistant_turn": assistant_turn,
                "turns": updated_turns,
                "score_result": result,
                "saved_path": str(saved_path.relative_to(REPO_ROOT)),
            },
            status=200,
        )

    def handle_native_capture(self) -> None:
        try:
            payload = self.read_json_body()
            turns = payload.get("turns")
            if not isinstance(turns, list):
                raise ValueError("turns must be an array.")
            conversation_id = str(payload.get("conversation_id") or native_capture_id(payload))
            user_id = str(payload.get("user_id") or payload.get("participant_id") or "native-participant")
            metadata = {
                "capture_lane": payload.get("capture_lane", "instrumented_native_capture"),
                "capture_source": payload.get("capture_source", "capture_client"),
                "source_url": payload.get("source_url"),
                "source_title": payload.get("source_title"),
                "device_platform": payload.get("device_platform"),
                "app_package": payload.get("app_package"),
                "provider_hint": payload.get("provider_hint"),
                "capture_quality": payload.get("capture_quality"),
                "captured_at": datetime.now(timezone.utc).isoformat(),
                **payload.get("conversation_metadata", {}),
            }
            score_request = {
                "conversation_id": conversation_id,
                "user_id": user_id,
                "conversation_metadata": metadata,
                "turns": turns,
            }
            result = score_conversation(score_request) if has_user_turn(turns) else None
            saved = save_native_capture(conversation_id, score_request, result)
        except Exception as error:
            self.respond_json({"error": str(error)}, status=400)
            return

        latest_trace = None
        if result and result.get("confidence_trace"):
            latest_trace = result["confidence_trace"][-1]
        self.respond_json(
            {
                "status": "captured",
                "conversation_id": conversation_id,
                "turn_count": len(turns),
                "saved_path": str(saved.relative_to(REPO_ROOT)),
                "latest_trace": latest_trace,
            },
            status=200,
        )

    def read_json_body(self) -> dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)
        payload = json.loads(raw_body.decode("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Request body must be a JSON object.")
        return payload

    def respond_json(self, payload: dict[str, Any], status: int) -> None:
        encoded = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def respond_file(self, path: Path) -> None:
        try:
            resolved = path.resolve()
            resolved.relative_to(FRONTEND_ROOT.resolve())
        except ValueError:
            self.respond_json({"error": "Not found."}, status=404)
            return

        if not resolved.is_file():
            self.respond_json({"error": "Not found."}, status=404)
            return

        content_type = mimetypes.guess_type(str(resolved))[0] or "application/octet-stream"
        encoded = resolved.read_bytes()
        self.send_response(200)
        self.send_cors_headers()
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def send_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format: str, *args: object) -> None:
        return


def has_user_turn(turns: list[dict[str, Any]]) -> bool:
    return any(str(turn.get("speaker", "")).lower() == "user" for turn in turns)


def native_capture_id(payload: dict[str, Any]) -> str:
    provider = slug(str(payload.get("provider_hint") or "native-ai"))
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"native-{provider}-{timestamp}"


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-") or "capture"


def save_native_capture(conversation_id: str, request: dict[str, Any], result: dict[str, Any] | None) -> Path:
    NATIVE_CAPTURE_ROOT.mkdir(parents=True, exist_ok=True)
    path = NATIVE_CAPTURE_ROOT / f"{slug(conversation_id)}.json"
    path.write_text(
        json.dumps(
            {
                "request": request,
                "result": result,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def save_router_run(conversation_id: str, request: dict[str, Any], response: dict[str, Any]) -> Path:
    ROUTER_RUN_ROOT.mkdir(parents=True, exist_ok=True)
    path = ROUTER_RUN_ROOT / f"{slug(conversation_id)}.json"
    path.write_text(
        json.dumps(
            {
                "request": request,
                "response": response,
                "saved_at": datetime.now(timezone.utc).isoformat(),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def list_router_runs() -> list[dict[str, Any]]:
    if not ROUTER_RUN_ROOT.exists():
        return []
    runs = []
    for path in sorted(ROUTER_RUN_ROOT.glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        request = payload.get("request", {})
        response = payload.get("response", {})
        score_result = response.get("score_result") or {}
        latest = None
        if score_result.get("confidence_trace"):
            latest = score_result["confidence_trace"][-1]
        runs.append(
            {
                "conversation_id": request.get("conversation_id"),
                "user_id": request.get("user_id"),
                "turn_count": len(request.get("turns", [])),
                "model_provider": response.get("model_provider"),
                "model_name": response.get("model_name"),
                "path": str(path.relative_to(REPO_ROOT)),
                "latest_trace": latest,
                "request": request,
                "response": response,
            }
        )
    return runs[:20]


    if not NATIVE_CAPTURE_ROOT.exists():
        return []
    captures = []
    for path in sorted(NATIVE_CAPTURE_ROOT.glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        request = payload.get("request", {})
        result = payload.get("result") or {}
        latest = None
        if result.get("confidence_trace"):
            latest = result["confidence_trace"][-1]
        captures.append(
            {
                "conversation_id": request.get("conversation_id"),
                "user_id": request.get("user_id"),
                "turn_count": len(request.get("turns", [])),
                "source_url": request.get("conversation_metadata", {}).get("source_url"),
                "provider_hint": request.get("conversation_metadata", {}).get("provider_hint"),
                "path": str(path.relative_to(REPO_ROOT)),
                "latest_trace": latest,
                "request": request,
                "result": result,
            }
        )
    return captures[:20]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the confidence evaluation frontend.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8090)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), FrontendHandler)
    print(f"Serving confidence evaluation frontend on http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
