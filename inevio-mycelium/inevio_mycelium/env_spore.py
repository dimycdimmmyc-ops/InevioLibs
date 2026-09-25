"""EnvSpore — обёртка над SporeBridge."""
from .environment import Environment


class EnvSpore(Environment):
    """Environment через spore-bridge."""

    def __init__(self, bridge):
        self.bridge = bridge

    @property
    def name(self):
        return getattr(self.bridge, 'name', 'mycelium')

    def send(self, to, topic, data):
        try:
            return self.bridge.send(to, topic, data)
        except Exception as e:
            self.log('debug', 'send error: ' + str(e))
            return False

    def broadcast(self, topic, data):
        try:
            return self.bridge.broadcast(topic, data)
        except Exception as e:
            self.log('debug', 'broadcast error: ' + str(e))
            return 0

    def neighbors(self):
        try:
            return self.bridge.neighbors()
        except Exception:
            return []

    def discover(self):
        """Discovery через spore-net."""
        try:
            node = self.bridge.node
            if hasattr(node, 'найти_соседей'):
                result = node.найти_соседей()
                out = []
                for item in result:
                    if isinstance(item, tuple) and len(item) >= 1:
                        out.append(item[0])
                return out
        except Exception:
            pass
        return []

    def subscribe(self, topic, handler):
        try:
            self.bridge.subscribe(topic, handler)
        except Exception:
            pass

    def unsubscribe(self, topic):
        try:
            self.bridge.unsubscribe(topic)
        except Exception:
            pass

    def log(self, level, msg):
        try:
            from spore.core.life import _logger
            _logger(level, msg)
        except Exception:
            pass