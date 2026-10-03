"""МИКОРИЗАnet · Иммунная память: свой/чужой, обучение врагам."""
import math
import threading
import time

from .constants import IMMUNE_BLOCK_THRESHOLD, IMMUNE_DECAY


class ImmuneMemory:
    """Иммунная память: обучение врагам + толерантность."""

    def __init__(self, trust_backend=None):
        self._tb = trust_backend
        self._self = set()
        self._en = {}
        self._tol = {}
        self._lock = threading.RLock()

    def learn_self(self, node_id):
        with self._lock:
            self._self.add(node_id)

    def is_self(self, node_id):
        with self._lock:
            return node_id in self._self

    def tolerate(self, node_id, ttl=3600.0):
        with self._lock:
            self._tol[node_id] = time.time() + ttl

    def tolerated(self, node_id):
        with self._lock:
            return self._tol.get(node_id, 0.0) > time.time()

    def attack(self, node_id, severity=1.0):
        with self._lock:
            self._en[node_id] = self._en.get(node_id, 0.0) + severity

    def blocked(self, node_id):
        with self._lock:
            if node_id in self._self or self._tol.get(node_id, 0.0) > time.time():
                return False
            return self._en.get(node_id, 0.0) >= IMMUNE_BLOCK_THRESHOLD

    def decay_tick(self, dt):
        k = math.exp(-IMMUNE_DECAY * dt)
        now = time.time()
        with self._lock:
            for n in list(self._en.keys()):
                self._en[n] *= k
                if self._en[n] < 0.1:
                    del self._en[n]
            for n in list(self._tol.keys()):
                if self._tol[n] < now:
                    del self._tol[n]

    def stats(self):
        with self._lock:
            return {
                "self": len(self._self),
                "enemies": dict(self._en),
                "tolerated": len(self._tol),
            }