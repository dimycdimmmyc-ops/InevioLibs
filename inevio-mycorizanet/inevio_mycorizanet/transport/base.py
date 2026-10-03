"""Transport — абстрактный транспорт."""
from abc import ABC, abstractmethod


class Transport(ABC):
    """Абстрактный транспортный канал."""

    name = "abstract"

    def __init__(self):
        self.pheromone = 1.0
        self.success = 0
        self.failure = 0

    @abstractmethod
    def available(self):
        """Доступен ли транспорт."""
        ...

    @abstractmethod
    def send(self, host, port, data):
        """Отправить данные. True/False."""
        ...

    @abstractmethod
    def receive(self, timeout=0.5):
        """Принять данные. (addr, data) или None."""
        ...

    def properties(self):
        """Свойства транспорта."""
        return {
            "name": self.name,
            "speed": 1.0,
            "stealth": 0.0,
            "reliability": 0.5,
        }

    def on_success(self):
        self.success += 1
        self.pheromone = min(10.0, self.pheromone + 0.2)

    def on_failure(self):
        self.failure += 1
        self.pheromone = max(0.01, self.pheromone * 0.5)

    def evaporate(self, dt, rate=0.02):
        import math
        self.pheromone *= math.exp(-rate * dt)

    def stats(self):
        total = self.success + self.failure
        rate = self.success / float(total) if total > 0 else 0.0
        return {
            "name": self.name,
            "pheromone": round(self.pheromone, 3),
            "success": self.success,
            "failure": self.failure,
            "success_rate": round(rate, 3),
            "available": self.available(),
        }