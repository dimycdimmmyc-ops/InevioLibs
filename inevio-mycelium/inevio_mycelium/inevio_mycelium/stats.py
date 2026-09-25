"""Mycelium stats."""
import time
import threading

from .helpers import _copy


class MyceliumStats:
    """Статистика грибницы."""

    def __init__(self):
        self._lock = threading.Lock()
        self._data = {
            'cycles': 0,
            'scouts': 0,
            'found': 0,
            'attached': 0,
            'penetrated': 0,
            'maps_taught': 0,
            'maps_merged': 0,
            'nodes_from_merge': 0,
            'max_depth': 0,
            'started_at': time.time(),
        }

    def inc(self, key, n=1):
        with self._lock:
            self._data[key] = self._data.get(key, 0) + n

    def set(self, key, val):
        with self._lock:
            self._data[key] = val

    def get(self, key, default=0):
        with self._lock:
            return self._data.get(key, default)

    def to_dict(self):
        with self._lock:
            return _copy(self._data)