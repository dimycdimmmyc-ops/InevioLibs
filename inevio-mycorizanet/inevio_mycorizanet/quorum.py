"""МИКОРИЗАnet · Уровень 5 — Кворум: концентрация сигналов."""
import math
import threading

from .constants import QUORUM_THRESHOLD, QUORUM_DECAY, QUORUM_HYSTERESIS


class QuorumSensor:
    """Кворум-сенсинг: порог концентрации вместо команд."""

    def __init__(self):
        self._c = {}
        self._fired = set()
        self.on_quorum = []
        self._lock = threading.RLock()

    def signal(self, topic, amount=1.0):
        with self._lock:
            self._c[topic] = self._c.get(topic, 0.0) + amount
            if self._c[topic] >= QUORUM_THRESHOLD and topic not in self._fired:
                self._fired.add(topic)
                for cb in list(self.on_quorum):
                    try:
                        cb(topic, self._c[topic])
                    except Exception:
                        pass

    def tick(self, dt):
        k = math.exp(-QUORUM_DECAY * dt)
        with self._lock:
            for t in list(self._c.keys()):
                self._c[t] *= k
                if t in self._fired and self._c[t] < QUORUM_THRESHOLD * QUORUM_HYSTERESIS:
                    self._fired.discard(t)

    def reached(self, topic):
        with self._lock:
            return topic in self._fired

    def concentrations(self):
        with self._lock:
            return dict(self._c)