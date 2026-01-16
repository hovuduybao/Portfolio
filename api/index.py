from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent
DOC_DIR = BASE_DIR / "doc"


def serve_file(handler, file_path: Path, content_type: str) -> None:
    try:
        with file_path.open("rb") as fh:
            data = fh.read()
        handler.send_response(200)
        handler.send_header("Content-Type", content_type)
        handler.send_header("Content-Length", str(len(data)))
        handler.end_headers()
        handler.wfile.write(data)
    except FileNotFoundError:
        handler.send_response(404)
        handler.end_headers()
    except OSError:
        handler.send_response(500)
        handler.end_headers()


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/cv.pdf":
            serve_file(self, DOC_DIR / "cv.pdf", "application/pdf")
            return
        if path == "/portfolio.pdf":
            serve_file(self, DOC_DIR / "portfolio.pdf", "application/pdf")
            return
        if path == "/cert_scrum_master.pdf":
            serve_file(self, DOC_DIR / "cert_scrum_master.pdf", "application/pdf")
            return
        if path == "/ldr_cnrs.pdf":
            serve_file(self, DOC_DIR / "ldr_cnrs.pdf", "application/pdf")
            return
        if path == "/ldr_optimiz_network.pdf":
            serve_file(self, DOC_DIR / "ldr_optimiz_network.pdf", "application/pdf")
            return
        if path == "/profile-photo.png":
            serve_file(self, DOC_DIR / "profile-photo.png", "image/png")
            return

        # Serve the main HTML page
        serve_file(self, DOC_DIR / "index.html", "text/html; charset=utf-8")

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        # Quieter logs in Vercel/runtime.
        return


def run_local(port: int = 8000) -> None:
    server_address = ("", port)
    httpd = HTTPServer(server_address, handler)
    print(f"Serving portfolio on http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    run_local(port=8686)
