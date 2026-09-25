"""Универсальная почва для ПК — UDP через localhost или сеть."""
import socket
from .base import Почва


class ПочваSocket(Почва):
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.setblocking(False)
        self._peers = set()
        self._тип = 'internet'

    def тип(self):
        return self._тип

    def пористость(self):
        return 0.5

    def питательность(self):
        return 0.5

    def отправить(self, кому, данные):
        if isinstance(данные, str):
            данные = данные.encode('utf-8')
        self.sock.sendto(данные, кому)
        self._peers.add(кому)

    def получить(self):
        try:
            данные, адрес = self.sock.recvfrom(65535)
            self._peers.add(адрес)
            return адрес, данные.decode('utf-8')
        except BlockingIOError:
            return None

    def соседи(self):
        return list(self._peers)