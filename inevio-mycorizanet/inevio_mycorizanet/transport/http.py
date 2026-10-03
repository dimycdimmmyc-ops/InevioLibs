"""HTTP-транспорт: туннель через HTTP-заголовки."""
import base64
import json
import urllib.request
from .base import Transport


class HTTPTransport(Transport):
    name = "http"

    def __init__(self, user_agent="Mozilla/5.0"):
        super().__init__()
        self.user_agent = user_agent
        self._inbox = []

    def available(self):
        try:
            urllib.request.urlopen("http://example.com", timeout=2)
            return True
        except Exception:
            return False

    def send(self, host, port, data):
        try:
            if isinstance(data, str):
                data = data.encode("utf-8")
            encoded = base64.b64encode(data).decode()
            url = "http://%s:%d/overlay" % (host, port)
            req = urllib.request.Request(url, method="POST",
                headers={
                    "User-Agent": self.user_agent,
                    "Content-Type": "application/octet-stream",
                    "X-Overlay-Data": encoded[:200],
                },
                data=data)
            urllib.request.urlopen(req, timeout=3)
            return True
        except Exception:
            return False

    def receive(self, timeout=0.5):
        if self._inbox:
            return self._inbox.pop(0)
        return None

    def properties(self):
        return {"name": self.name, "speed": 0.5, "stealth": 0.95, "reliability": 0.85}