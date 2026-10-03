"""ICMP-транспорт: туннель через ping."""
import subprocess
import sys
from .base import Transport


class ICMPTransport(Transport):
    name = "icmp"

    def __init__(self):
        super().__init__()
        self._inbox = []

    def available(self):
        try:
            if sys.platform == "win32":
                cmd = ["ping", "-n", "1", "127.0.0.1"]
            else:
                cmd = ["ping", "-c", "1", "127.0.0.1"]
            r = subprocess.run(cmd, capture_output=True, timeout=2)
            return r.returncode == 0
        except Exception:
            return False

    def send(self, host, port, data):
        try:
            if isinstance(data, str):
                data = data.encode("utf-8")
            payload_hex = data.hex()[:32]
            if sys.platform == "win32":
                cmd = ["ping", "-n", "1", "-w", "1000", "-l", "32", "-p", payload_hex, host]
            else:
                cmd = ["ping", "-c", "1", "-W", "1", "-p", payload_hex, host]
            r = subprocess.run(cmd, capture_output=True, timeout=3)
            return r.returncode == 0
        except Exception:
            return False

    def receive(self, timeout=0.5):
        if self._inbox:
            return self._inbox.pop(0)
        return None

    def properties(self):
        return {"name": self.name, "speed": 0.3, "stealth": 0.7, "reliability": 0.5}