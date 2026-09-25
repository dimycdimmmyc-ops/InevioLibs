"""Почва LoRa — дальняя связь, низкая скорость."""
from .base import Почва


class ПочваLoRa(Почва):
    def __init__(self, частота="433"):
        self.частота = частота
        self._peers = set()
        self.активна = False  # требует LoRa-модуля

    def тип(self):
        return 'lora'

    def пористость(self):
        # LoRa — очень плотная почва, почти нет пор
        return 0.1 if self.активна else 0.0

    def питательность(self):
        # Очень низкая скорость (0.3-37.5 kbps)[citation:9]
        return 0.1

    def отправить(self, кому, данные):
        self._peers.add(кому)

    def получить(self):
        return None

    def соседи(self):
        return list(self._peers)