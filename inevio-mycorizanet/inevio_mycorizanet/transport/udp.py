"""UDP-транспорт."""
import socket
from .base import Transport


class UDPTransport(Transport):
    name = "udp"

    def __init__(self, port=0):
        super().__init__()
        self.port = port
        self.sock = None
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if port:
                self.sock.bind(("0.0.0.0", port))
            self.sock.setblocking(False)
        except Exception:
            self.sock = None

    def available(self):
        return self.sock is not None

    def send(self, host, port, data):
        if not self.sock:
            return False
        try:
            if isinstance(data, str):
                data = data.encode("utf-8")
            self.sock.sendto(data, (host, port))
            return True
        except Exception:
            return False

    def receive(self, timeout=0.5):
        if not self.sock:
            return None
        try:
            data, addr = self.sock.recvfrom(65535)
            return (addr, data)
        except BlockingIOError:
            return None
        except Exception:
            return None

    def properties(self):
        return {"name": self.name, "speed": 0.9, "stealth": 0.2, "reliability": 0.6}

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None