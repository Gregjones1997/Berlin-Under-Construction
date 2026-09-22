"""Loopback-only dependency-failure fixture. Run from the repository root.

Serves the generated public export, returning 503 only for the model manifest.
Does not change the normal preview or production. No private files are served.
"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


class FailureHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / "web/dist"), **kwargs)

    def do_GET(self):
        if self.path.split("?")[0] == "/atlas/model.json":
            self.send_error(503, "Synthetic review failure")
            return
        super().do_GET()


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 48769), FailureHandler).serve_forever()
