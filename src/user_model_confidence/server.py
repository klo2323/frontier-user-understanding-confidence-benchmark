from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from user_model_confidence.embeddings import check_embedding_health
from user_model_confidence.scorer import score_conversation


class ScoreConversationHandler(BaseHTTPRequestHandler):
    server_version = "UserUnderstandingConfidenceServer/0.1"

    def do_POST(self) -> None:
        if self.path == "/score-conversation":
            try:
                payload = self.read_json_body()
                result = score_conversation(payload)
            except Exception as error:
                self.respond_json({"error": str(error)}, status=400)
                return

            self.respond_json(result, status=200)
            return

        self.respond_json({"error": "Not found."}, status=404)

    def do_GET(self) -> None:
        if self.path == "/health":
            self.respond_json({"status": "ok"}, status=200)
            return
        if self.path == "/embedding-health":
            result = check_embedding_health()
            self.respond_json(result, status=200 if result["ok"] else 503)
            return
        self.respond_json({"error": "Not found."}, status=404)

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
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args: object) -> None:
        return


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the local score-conversation HTTP server."
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args(argv)

    server = ThreadingHTTPServer((args.host, args.port), ScoreConversationHandler)
    print(f"Serving /score-conversation on http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        server.server_close()

    return 0
