"""REST-микросервис SuperNode (stdlib only). Порт по умолчанию 8701."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .manager import SuperNodeManager
MANAGER = SuperNodeManager()

class _Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)
    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}")
    def do_GET(self):
        if self.path in ("/super_nodes", "/stats"):
            self._send(200, {"success": True, **MANAGER.get_stats()})
        else:
            self._send(404, {"success": False, "error": "not_found"})
    def do_POST(self):
        d = self._body()
        if self.path == "/promote":
            ok = MANAGER.promote(d.get("node", {}),
                                 d.get("evolution_stats"), d.get("delivery_stats"))
            self._send(200, {"success": ok})
        elif self.path == "/apply":
            self._send(200, {"success": True, "applied": MANAGER.apply_experience(d)})
        elif self.path == "/broadcast":
            p = MANAGER.broadcast_payload(d.get("node_id", ""), d.get("interval", 60.0))
            self._send(200, {"success": p is not None, "payload": p})
        else:
            self._send(404, {"success": False, "error": "not_found"})
    def log_message(self, *a):
        pass

def main(host="127.0.0.1", port=8701):
    ThreadingHTTPServer((host, port), _Handler).serve_forever()

if __name__ == "__main__":
    main()
