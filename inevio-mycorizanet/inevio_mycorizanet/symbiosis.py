"""МИКОРИЗАnet · Уровень 4 — Симбиоз: оба выигрывают или разрыв."""
import threading
import time

from .constants import SYMBIOSIS_MIN_MUTUAL, SYMBIOSIS_PRUNE_AFTER


class SymbiosisLedger:
    """Ledger взаимной выгоды."""

    def __init__(self):
        self._l = {}
        self._lock = threading.RLock()

    def _e(self, peer):
        return self._l.setdefault(peer, {
            "given": 0.0, "received": 0.0, "last": time.time(),
        })

    def record_given(self, peer, value=1.0):
        with self._lock:
            e = self._e(peer)
            e["given"] += value
            e["last"] = time.time()

    def record_received(self, peer, value=1.0):
        with self._lock:
            e = self._e(peer)
            e["received"] += value
            e["last"] = time.time()

    def fairness(self, peer):
        with self._lock:
            e = self._l.get(peer)
            if not e:
                return 0.0
            g, r = e["given"], e["received"]
            return min(g, r) / max(g, r) if max(g, r) > 0 else 0.0

    def mutual(self, peer):
        with self._lock:
            e = self._l.get(peer)
            return bool(e and e["given"] >= SYMBIOSIS_MIN_MUTUAL
                        and e["received"] >= SYMBIOSIS_MIN_MUTUAL)

    def partners(self):
        with self._lock:
            return [p for p in self._l if self.mutual(p)]

    def prune(self, now=None):
        now = now or time.time()
        removed = []
        with self._lock:
            for p in list(self._l.keys()):
                e = self._l[p]
                one_sided = ((e["given"] < SYMBIOSIS_MIN_MUTUAL) !=
                             (e["received"] < SYMBIOSIS_MIN_MUTUAL))
                if one_sided and now - e["last"] > SYMBIOSIS_PRUNE_AFTER:
                    removed.append(p)
                    del self._l[p]
        return removed

    def snapshot(self):
        with self._lock:
            return {p: dict(e) for p, e in self._l.items()}