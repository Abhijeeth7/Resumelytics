from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict

from scoring_service import evaluate_resume_against_jd


class _Handler(BaseHTTPRequestHandler):
    def _write_json(self, status_code: int, payload: Dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._write_json(200, {"ok": True})
            return
        self._write_json(404, {"error": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/score":
            self._write_json(404, {"error": "Not found"})
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8")

        try:
            body = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            self._write_json(400, {"error": "Invalid JSON"})
            return

        resume_text = str(body.get("resume_text", "")).strip()
        jd_text = str(body.get("jd_text", "")).strip()
        candidate_experience = body.get("candidate_experience")
        if candidate_experience is not None:
            try:
                candidate_experience = int(candidate_experience)
            except (TypeError, ValueError):
                self._write_json(
                    400,
                    {"error": "candidate_experience must be an integer or null"},
                )
                return

        if not resume_text or not jd_text:
            self._write_json(
                400,
                {"error": "resume_text and jd_text are required"},
            )
            return

        result = evaluate_resume_against_jd(
            resume_text=resume_text,
            jd_text=jd_text,
            candidate_experience=candidate_experience,
        )
        self._write_json(200, result)


def run_server(host: str = "127.0.0.1", port: int = 8787) -> None:
    server = ThreadingHTTPServer((host, port), _Handler)
    print(f"Resumelytics API running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
