"""Почва Bluetooth (BLE Mesh)."""
from .base import Почва

try:
    from winrt.windows.devices.bluetooth import BluetoothLEDevice
    from winrt.windows.devices.bluetooth.genericattributeprofile import GattServiceProvider
    WINRT_BT = True
except ImportError:
    WINRT_BT = False


class ПочваBluetooth(Почва):
    def __init__(self, имя_узла="spore-node"):
        self.имя_узла = имя_узла
        self._peers = set()
        self.активна = WINRT_BT

    def тип(self):
        return 'bluetooth'

    def пористость(self):
        # BLE — пористая почва, можно встроиться
        return 0.8 if self.активна else 0.0

    def питательность(self):
        # Низкая скорость, но очень экономичная
        return 0.4

    def отправить(self, кому, данные):
        self._peers.add(кому)

    def получить(self):
        return None

    def соседи(self):
        return list(self._peers)