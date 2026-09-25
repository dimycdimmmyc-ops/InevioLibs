"""
Почва Wi-Fi Direct — реальная реализация.
"""
import socket
import threading
from .base import Почва

try:
    from winrt.windows.devices.wifidirect import WiFiDirectAdvertisementPublisher
    WINRT_ЕСТЬ = True
    print("[INIT] winrt.wifidirect импортирован")
except ImportError as e:
    WINRT_ЕСТЬ = False
    print("[INIT] winrt.wifidirect НЕ доступен: " + str(e))


class ПочваWiFiDirect(Почва):
    def __init__(self, имя_сети="SPORE-MESH", пароль="spore1234",
                 роль="publisher", tcp_port=50000):
        print("[INIT] ПочваWiFiDirect: роль=" + роль + ", порт=" + str(tcp_port) + ", WINRT_ЕСТЬ=" + str(WINRT_ЕСТЬ))

        self.имя_сети = имя_сети
        self.пароль = пароль
        self.роль = роль
        self.tcp_port = tcp_port

        self._peers = set()
        self._входящие = []

        self.wifi_direct_активен = False
        if WINRT_ЕСТЬ and роль == "publisher":
            self._запустить_wifi_direct_publisher()

        self.tcp_активен = False
        self._запустить_tcp_сервер()

    def тип(self):
        return 'wifi_direct'

    def пористость(self):
        if self.wifi_direct_активен:
            return 0.85
        if self.tcp_активен:
            return 0.5
        return 0.0

    def питательность(self):
        return 0.9

    def отправить(self, кому, данные):
        """
        ВАЖНО: используем порт ПОЛУЧАТЕЛЯ (кому[1]),
        а не свой (self.tcp_port).
        """
        print("[SEND] -> " + str(кому) + " (порт получателя: " + str(кому[1]) + ")")
        if isinstance(данные, str):
            данные = данные.encode('utf-8')
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2.0)
                s.connect((кому[0], кому[1]))   # ← ПОРТ ПОЛУЧАТЕЛЯ
                s.sendall(данные)
            self._peers.add(кому)
            print("[SEND] OK, " + str(len(данные)) + " байт")
            return True
        except Exception as e:
            print("[SEND] ОШИБКА: " + str(e))
            return False

    def получить(self):
        print("[RECV] получить() вызван, в очереди: " + str(len(self._входящие)) + " (порт " + str(self.tcp_port) + ")")
        if self._входящие:
            пакет = self._входящие.pop(0)
            print("[RECV] Выдан пакет: " + str(len(пакет[1])) + " байт")
            return пакет
        return None

    def соседи(self):
        return list(self._peers)

    def _запустить_wifi_direct_publisher(self):
        try:
            self.publisher = WiFiDirectAdvertisementPublisher()
            self.publisher.start()
            self.wifi_direct_активен = True
            print("[WFD] Publisher запущен: " + self.имя_сети)
        except Exception as e:
            print("[WFD] Publisher ошибка: " + str(e))
            self.wifi_direct_активен = False

    def _запустить_tcp_сервер(self):
        порт_этого_объекта = self.tcp_port

        def сервер():
            try:
                srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                srv.bind(('0.0.0.0', порт_этого_объекта))
                srv.listen(5)
                srv.settimeout(0.5)
                self.tcp_активен = True
                print("[TCP] Сервер слушает порт " + str(порт_этого_объекта))
                while True:
                    try:
                        conn, адрес = srv.accept()
                        данные = conn.recv(65535)
                        conn.close()
                        if данные:
                            self._peers.add(адрес)
                            self._входящие.append(
                                (адрес, данные.decode('utf-8', errors='replace'))
                            )
                            print("[TCP:" + str(порт_этого_объекта) + "] Принято " + str(len(данные)) + " байт от " + str(адрес))
                    except socket.timeout:
                        continue
                    except Exception as e:
                        print("[TCP] Ошибка accept: " + str(e))
                        break
            except Exception as e:
                print("[TCP] Сервер НЕ поднялся: " + str(e))
                self.tcp_активен = False

        threading.Thread(target=сервер, daemon=True).start()