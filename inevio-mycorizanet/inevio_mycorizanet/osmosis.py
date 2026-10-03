"""МИКОРИЗАnet · Уровень 6 — Осмос: поток по градиенту нагрузки."""
import threading
import time
from collections import deque

from .constants import (
    OSMOSIS_CAPACITY, OSMOSIS_BUFFER_MAX, OSMOSIS_NEIGHBOR_TTL,
)


class OsmoticBalancer:
    """Поток по градиенту + буфер сглаживания."""

    def __init__(self):
        self.load = 0.0
        self._nb = {}
        self._buf = deque()
        self._lock = threading.RLock()

    def set_load(self, v):
        self.load = float(v)

    def pressure(self):
        with self._lock:
            return len(self._buf) / float(OSMOSIS_BUFFER_MAX)

    def report_neighbor(self, nid, load):
        with self._lock:
            self._nb[nid] = (float(load), time.time())

    def downhill(self, exclude=()):
        now = time.time()
        with self._lock:
            cand = [n for n, (l, ts) in self._nb.items()
                    if n not in exclude and now - ts < OSMOSIS_NEIGHBOR_TTL]
            if not cand:
                return None
            return min(cand, key=lambda n: self._nb[n][0])

    def gradient(self, nid):
        with self._lock:
            return self.load - self._nb.get(nid, (0.0, 0.0))[0]

    def accept(self, item):
        with self._lock:
            if len(self._buf) >= OSMOSIS_BUFFER_MAX:
                return False
            self._buf.append(item)
            return True

    def drain(self, n=8):
        out = []
        with self._lock:
            while self._buf and len(out) < n:
                out.append(self._buf.popleft())
        return out