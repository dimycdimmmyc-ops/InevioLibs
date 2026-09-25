"""EnvMock — для тестов без сети."""
from .environment import Environment


class EnvMock(Environment):
    """Mock Environment."""

    def __init__(self, name='mock'):
        self._name = name
        self._neighbors = []
        self._inbox = []
        self._subscriptions = {}
        self._sent = []
        self._broadcasts = []
        self._discover_result = []
        self._events = []

    @property
    def name(self):
        return self._name

    def send(self, to, topic, data):
        self._sent.append((to, topic, data))
        # Автоматически доставить в inbox
        self._inbox.append((to, topic, data))
        # Вызвать подписку если есть
        handler = self._subscriptions.get(topic)
        if handler:
            try:
                handler(data, self._name)
            except Exception:
                pass
        return True

    def broadcast(self, topic, data):
        self._broadcasts.append((topic, data))
        handler = self._subscriptions.get(topic)
        if handler:
            try:
                handler(data, self._name)
            except Exception:
                pass
        return len(self._neighbors)

    def neighbors(self):
        return list(self._neighbors)

    def discover(self):
        return list(self._discover_result)

    def subscribe(self, topic, handler):
        self._subscriptions[topic] = handler

    def unsubscribe(self, topic):
        self._subscriptions.pop(topic, None)

    def log(self, level, msg):
        self._events.append((level, msg))

    # Для тестов
    def add_neighbor(self, addr):
        if addr not in self._neighbors:
            self._neighbors.append(addr)

    def add_discover(self, addr):
        if addr not in self._discover_result:
            self._discover_result.append(addr)