"""REST-микросервис SporeRecon. Порт по умолчанию 8702."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from .recon import full_recon, neighbors_estimate, identify_isp

class _Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)
        if self.path.startswith("/recon"):
            self._send(200, {"success": True,
                             "findings": full_recon(q.get("ssid", [""])[0],
                                                    q.get("bssid", [""])[0])})
        elif self.path == "/neighbors":
            self._send(200, {"success": True, "neighbors": neighbors_estimate()})
        elif self.path == "/isp":
            self._send(200, {"success": True, "isp": identify_isp()})
        else:
            self._send(404, {"success": False, "error": "not_found"})
    def log_message(self, *a):
        pass

def main(host="127.0.0.1", port=8702):
    ThreadingHTTPServer((host, port), _Handler).serve_forever()

if __name__ == "__main__":
    main()
