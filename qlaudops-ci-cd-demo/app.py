"""Dependency-free HTTP server for the QlaudOps CloudOps demo dashboard."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
SERVICES = [
    {"name": "Production API", "type": "Application", "status": "Healthy", "uptime": "99.98%", "region": "ap-south-1", "latency": "84 ms"},
    {"name": "Payments Worker", "type": "Background worker", "status": "Healthy", "uptime": "99.95%", "region": "ap-south-1", "latency": "112 ms"},
    {"name": "Backup Scheduler", "type": "Backup & recovery", "status": "Warning", "uptime": "98.70%", "region": "ap-south-1", "latency": "—"},
    {"name": "Monitoring Agent", "type": "Observability", "status": "Healthy", "uptime": "99.99%", "region": "us-east-1", "latency": "41 ms"},
]

class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            return self._json({"status": "healthy", "service": "qlaudops-cloudops-dashboard"})
        if path == "/api/services":
            return self._json(SERVICES)
        if path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def _json(self, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        # Keep logs concise for demo terminals and container output.
        print(f"[{self.log_date_time_string()}] {fmt % args}")


def create_server(host="0.0.0.0", port=5000):
    return ThreadingHTTPServer((host, port), DashboardHandler)


if __name__ == "__main__":
    server = create_server()
    print("QlaudOps CloudOps dashboard running at http://127.0.0.1:5000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down dashboard...")
    finally:
        server.server_close()
