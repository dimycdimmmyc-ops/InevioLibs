"""Почва Wi-Fi Aware (NAN) — neighbour aware networking."""
from .base import Почва


class ПочваWiFiAware(Почва):
    def __init__(self, cluster_id=None):
        self.cluster_id = cluster_id or "spore-cluster-1"
        self._peers = set()
        self.активна = False  # на Windows обычно недоступна

    def тип(self):
        return 'wifi_aware'

    def пористость(self):
        return 0.75 if self.активна else 0.0

    def питательность(self):
        # Высокая (сравнима с Wi-Fi Direct)[citation:34]
        return 0.85

    def отправить(self, кому, данные):
        self._peers.add(кому)

    def получить(self):
        return None

    def соседи(self):
        return list(self._peers)