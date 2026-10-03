"""МИКОРИЗАnet · Уровень 2 — Мембрана: антиген + потенциал."""
import hashlib
import hmac
import struct
import threading
import time

from .constants import MEMBRANE_SLOT, MEMBRANE_MAX_AGE


class Membrane:
    """Полупроницаемая мембрана: антиген + потенциал."""

    def __init__(self, secret, self_id, rest=0.5):
        self.secret = secret if isinstance(secret, bytes) else str(secret).encode()
        self.self_id = self_id
        self._pot = {self_id: rest}
        self._lock = threading.RLock()

    def _tag(self, peer_id, slot):
        a, b = sorted((self.self_id, peer_id))
        return hmac.new(
            self.secret,
            ("ag:%s:%s:%d" % (a, b, slot)).encode(),
            hashlib.sha256
        ).digest()[:16]

    def seal(self, payload, peer_id):
        slot = int(time.time() // MEMBRANE_SLOT)
        return struct.pack(">Q", slot) + self._tag(peer_id, slot) + payload

    def verify(self, blob, peer_id, max_age=MEMBRANE_MAX_AGE):
        if len(blob) < 24:
            return False
        slot = struct.unpack(">Q", blob[:8])[0]
        now = int(time.time() // MEMBRANE_SLOT)
        if slot > now or (now - slot) * MEMBRANE_SLOT > max_age:
            return False
        return hmac.compare_digest(blob[8:24], self._tag(peer_id, slot))

    def payload(self, blob):
        return blob[24:]

    def charge(self, node_id, delta):
        with self._lock:
            self._pot[node_id] = min(1.0, max(0.0, self._pot.get(node_id, 0.5) + delta))
            return self._pot[node_id]

    def potential(self, node_id):
        with self._lock:
            return self._pot.get(node_id, 0.5)

    def permeable(self, src, dst):
        dp = self.potential(src) - self.potential(dst)
        if dp >= -0.05:
            return True, 0.0
        cost = -dp
        if self.potential(src) >= cost:
            self.charge(src, -cost)
            return True, cost
        return False, cost