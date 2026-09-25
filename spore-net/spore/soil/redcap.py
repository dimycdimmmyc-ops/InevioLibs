"""Почва 5G RedCap — сотовая IoT-связь."""
from .base import Почва


class ПочваRedCap(Почва):
    def __init__(self, оператор=None):
        self.оператор = оператор
        self._peers = set()
        self.активна = False  # требует RedCap-модема

    def тип(self):
        return '5g_redcap'

    def пористость(self):
        # Сотовая сеть — плотная почва
        return 0.3 if self.активна else 0.0

    def питательность(self):
        # Средняя скорость (227/122 Mbps)[citation:2]
        return 0.7

    def отправить(self, кому, данные):
        self._peers.add(кому)

    def получить(self):
        return None

    def соседи(self):
        return list(self._peers)