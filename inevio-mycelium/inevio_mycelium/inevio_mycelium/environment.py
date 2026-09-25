"""Mycelium Environment — абстрактный интерфейс к внешнему миру.

Mycelium НЕ знает про spore-net напрямую.
Работает через Environment.
"""
from abc import ABC, abstractmethod


class Environment(ABC):
    """Абстрактный интерфейс."""

    @property
    @abstractmethod
    def name(self):
        """Имя узла."""
        ...

    @abstractmethod
    def send(self, to, topic, data):
        """Отправить сообщение."""
        ...

    @abstractmethod
    def broadcast(self, topic, data):
        """Разослать всем."""
        ...

    @abstractmethod
    def neighbors(self):
        """Список известных адресов."""
        ...

    @abstractmethod
    def discover(self):
        """Найти новых соседей. Возвращает список."""
        ...

    @abstractmethod
    def subscribe(self, topic, handler):
        """Подписаться на топик."""
        ...

    @abstractmethod
    def unsubscribe(self, topic):
        ...

    @abstractmethod
    def log(self, level, msg):
        ...