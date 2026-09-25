"""Mycelium memory — узлы, глубина, карты."""
import time
import threading
from collections import deque

from .constants import MEMORY_NODES_MAX, MEMORY_PHASE_LOG_MAX


class MyceliumMemory:
    """Память грибницы."""

    def __init__(self):
        self._lock = threading.Lock()
        self.nodes = {}          # addr -> {addr, type, depth, source, ...}
        self.attached = {}       # addr -> node (закреплённые)
        self.depth = {}          # addr -> int
        self.phase_log = deque(maxlen=MEMORY_PHASE_LOG_MAX)
        self._new_since_teach = 0

    def add_node(self, addr, node):
        """Добавить узел. True если новый."""
        if not addr:
            return False
        with self._lock:
            if addr in self.nodes:
                self.nodes[addr]['last_seen'] = time.time()
                return False
            if len(self.nodes) >= MEMORY_NODES_MAX:
                oldest = min(self.nodes.items(),
                             key=lambda x: x[1].get('last_seen', 0))
                del self.nodes[oldest[0]]
            node['addr'] = addr
            node['discovered_at'] = node.get('discovered_at', time.time())
            node['last_seen'] = time.time()
            self.nodes[addr] = node
            self._new_since_teach += 1
            return True

    def attach(self, addr, node):
        """Закрепиться на узле."""
        with self._lock:
            if addr in self.attached:
                return False
            self.attached[addr] = node
            cur = self.depth.get(addr, 0)
            self.depth[addr] = cur + 1
            return True

    def get_node(self, addr):
        with self._lock:
            return self.nodes.get(addr, {})

    def get_all_nodes(self):
        with self._lock:
            return list(self.nodes.values())

    def get_recent_nodes(self, limit=100):
        with self._lock:
            items = list(self.nodes.items())
            items.sort(key=lambda x: x[1].get('discovered_at', 0), reverse=True)
            return [n for _, n in items[:limit]]

    def max_depth(self):
        with self._lock:
            if not self.depth:
                return 0
            return max(self.depth.values())

    def has_new_since_teach(self):
        with self._lock:
            return self._new_since_teach > 0

    def mark_taught(self):
        with self._lock:
            self._new_since_teach = 0

    def log_phase(self, phase, elapsed=0.0, extra=''):
        with self._lock:
            self.phase_log.append({
                'phase': phase, 'elapsed': elapsed,
                'extra': extra, 'ts': time.time(),
            })

    def get_stats(self):
        with self._lock:
            return {
                'nodes': len(self.nodes),
                'attached': len(self.attached),
                'depth_max': max(self.depth.values()) if self.depth else 0,
            }

    def get_phase_log(self, n=30):
        with self._lock:
            return list(self.phase_log)[-n:]