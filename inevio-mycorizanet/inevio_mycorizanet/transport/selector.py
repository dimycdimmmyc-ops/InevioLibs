"""TransportSelector — автономный выбор транспорта (слизевик)."""
import math
import threading


class TransportSelector:
    """
    Слизевик-подобный выбор транспорта.

    Перебирает транспорты, усиливает успешные, забывает неудачные.
    """

    def __init__(self, transports=None):
        self.transports = transports or []
        self.current = None
        self._lock = threading.RLock()

    def add(self, transport):
        with self._lock:
            self.transports.append(transport)

    def remove(self, transport):
        with self._lock:
            if transport in self.transports:
                self.transports.remove(transport)

    def choose(self, task=None):
        """Выбрать лучший транспорт."""
        with self._lock:
            available = [t for t in self.transports if t.available()]
        if not available:
            return None

        if task == "stealth":
            return max(available, key=lambda t: t.properties()["stealth"])
        if task == "speed":
            return max(available, key=lambda t: t.properties()["speed"])
        if task == "reliable":
            return max(available, key=lambda t: t.properties()["reliability"])

        # По умолчанию — феромонный выбор
        return max(available, key=lambda t: t.pheromone)

    def send(self, host, port, data, task=None):
        """Отправить через лучший транспорт."""
        t = self.choose(task)
        if not t:
            return {"status": "no_transport"}
        ok = t.send(host, port, data)
        if ok:
            t.on_success()
            self.current = t
            return {"status": "sent", "transport": t.name}
        else:
            t.on_failure()
            # Пробуем другой
            others = [x for x in self.transports if x is not t and x.available()]
            if not others:
                return {"status": "failed", "transport": t.name}
            return self.send(host, port, data, task)

    def tick(self, dt):
        """Затухание феромонов + переключение."""
        with self._lock:
            for t in self.transports:
                t.evaporate(dt)
            best = self.choose()
            if best and (not self.current or best.pheromone > self.current.pheromone * 1.5):
                self.current = best

    def stats(self):
        with self._lock:
            return {
                "current": self.current.name if self.current else None,
                "transports": [t.stats() for t in self.transports],
            }