"""МИКОРИЗАnet · Уровень 3 — Феромонные тропы."""
import math
import random
import threading

from .constants import (
    TRAIL_EVAPORATION, TRAIL_DEPOSIT,
    TRAIL_CAP, TRAIL_PRUNE, TRAIL_EXPLORE,
)


class TrailTable:
    """Феромонные маршруты: успех усиливает, неудача гасит."""

    def __init__(self):
        self._t = {}
        self._lock = threading.RLock()

    def deposit(self, dest, hop, amount=None, rtt=None):
        a = amount if amount is not None else TRAIL_DEPOSIT
        if rtt:
            a *= 1.0 / (1.0 + rtt)
        with self._lock:
            row = self._t.setdefault(dest, {})
            row[hop] = min(TRAIL_CAP, row.get(hop, 0.0) + a)

    def penalize(self, dest, hop, factor=0.5):
        with self._lock:
            row = self._t.get(dest, {})
            if hop in row:
                row[hop] *= factor

    def evaporate(self, dt):
        k = math.exp(-TRAIL_EVAPORATION * dt)
        with self._lock:
            for dest in list(self._t.keys()):
                row = self._t[dest]
                for hop in list(row.keys()):
                    row[hop] *= k
                    if row[hop] < TRAIL_PRUNE:
                        del row[hop]
                if not row:
                    del self._t[dest]

    def next_hop(self, dest, exclude=()):
        with self._lock:
            row = {h: v for h, v in self._t.get(dest, {}).items() if h not in exclude}
        return max(row, key=row.get) if row else None

    def choose(self, dest, explore=TRAIL_EXPLORE, exclude=()):
        with self._lock:
            row = {h: v for h, v in self._t.get(dest, {}).items() if h not in exclude}
        if not row:
            return None
        if random.random() < explore:
            return random.choice(list(row.keys()))
        return max(row, key=row.get)

    def snapshot(self):
        with self._lock:
            return {d: dict(r) for d, r in self._t.items()}