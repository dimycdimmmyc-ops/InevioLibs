"""TCP-транспорт."""
import socket
from .base import Transport


class TCPTransport(Transport):
    name = "tcp"

    def __init__(self, listen_port=0):
        super().__init__()
        self.listen_port = listen_port
        self.server = None
        self.client = None
        try:
            if listen_port:
                self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.server.bind(("0.0.0.0", listen_port))
                self.server.listen(5)
                self.server.setblocking(False)
        except Exception:
            self.server = None

    def available(self):
        return True

    def send(self, host, port, data):
        try:
            if isinstance(data, str):
                data = data.encode("utf-8")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2.0)
                s.connect((host, port))
                s.sendall(data)
            return True
        except Exception:
            return False

    def receive(self, timeout=0.5):
        if not self.server:
            return None
        try:
            conn, addr = self.server.accept()
            conn.settimeout(timeout)
            data = conn.recv(65535)
            conn.close()
            return (addr, data)
        except BlockingIOError:
            return None
        except Exception:
            return None

    def properties(self):
        return {"name": self.name, "speed": 0.7, "stealth": 0.3, "reliability": 0.95}

    def close(self):
        if self.server:
            try:
                self.server.close()
            except Exception:
                pass
            self.server = None