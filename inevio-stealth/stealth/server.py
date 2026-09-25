"""REST-микросервис Stealth. Порт по умолчанию 8704."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .engine import StealthEngine
ENG = StealthEngine()

class _Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        if self.path == "/stats":
            self._send(200, {"success": True, **ENG.get_stats()})
        elif self.path == "/channels":
            self._send(200, {"success": True, "channels": ENG.get_channels()})
        else:
            self._send(404, {"success": False, "error": "not_found"})
    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        d = json.loads(self.rfile.read(n) or b"{}")
        if self.path == "/send":
            self._send(200, ENG.send(d.get("payload", ""), d.get("target", "")))
        elif self.path == "/probe":
            self._send(200, {"success": True,
                             "results": ENG.probe(d.get("target", ""))})
        else:
            self._send(404, {"success": False, "error": "not_found"})
    def log_message(self, *a):
        pass

def main(host="127.0.0.1", port=8704):
    ThreadingHTTPServer((host, port), _Handler).serve_forever()

if __name__ == "__main__":
    main()
