"""Почва RFID/NFC — сверхближняя связь."""
from .base import Почва


class ПочваNFC(Почва):
    def __init__(self):
        self._peers = set()
        self.активна = False

    def тип(self):
        return 'nfc'

    def пористость(self):
        # NFC работает только в упор — очень плотная почва
        return 0.05 if self.активна else 0.0

    def питательность(self):
        # Низкая скорость (106-424 kbps)[citation:14]
        return 0.2

    def отправить(self, кому, данные):
        self._peers.add(кому)

    def получить(self):
        return None

    def соседи(self):
        return list(self._peers)


class ПочваRFID(Почва):
    def __init__(self, частота="UHF"):
        self.частота = частота  # LF, HF, UHF
        self._peers = set()
        self.активна = False

    def тип(self):
        return 'rfid'

    def пористость(self):
        return 0.2 if self.активна else 0.0

    def питательность(self):
        return 0.15

    def отправить(self, кому, данные):
        self._peers.add(кому)

    def получить(self):
        return None

    def соседи(self):
        return list(self._peers)