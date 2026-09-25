"""SporeBridge: transport between InevioLibs and spore-net."""
import threading
import time

from spore import SporeNode
from spore.soil import (
    ПочваSocket,
    ПочваWiFiDirect,
    ПочваBluetooth,
)


class SporeBridge:
    """
    Bridge between InevioLibs and spore-net.
    """

    def __init__(self, name, port=8700, direction='V', soils=None):
        self.name = name
        self.port = port

        if soils is None:
            soils = self._collect_soils(port)

        best = SporeNode.выбрать_почву(soils)
        if best is None:
            raise RuntimeError('No working soil found')

        self.soil = best
        self.node = SporeNode(best, имя=name, направление=direction)
        self._subscriptions = {}
        self._stop = threading.Event()
        self._thread = None
        self._breath_counter = 0

    @staticmethod
    def _collect_soils(port):
        soils = []
        try:
            soils.append(ПочваSocket('0.0.0.0', port))
        except Exception as e:
            print('[bridge] ПочваSocket failed: ' + str(e))
        return soils

    # ---------- PUBLIC API ----------

    def send(self, to, topic, data):
        packet = {
            'bridge': True,
            'from': self.name,
            'topic': topic,
            'payload': data,
        }
        return self.node.отправить(to, packet)

    def broadcast(self, topic, data, discovery_timeout=1.5):
        """
        Broadcast data to all known neighbours.
        If no neighbours — runs discovery via spore-net and waits.
        Returns number of neighbours the packet was sent to.
        """
        neighbours = self.neighbors()

        if not neighbours:
            try:
                self.node.найти_соседей()
            except Exception:
                pass
            time.sleep(discovery_timeout)
            neighbours = self.neighbors()

        if not neighbours:
            return 0

        sent = 0
        for neighbour in neighbours:
            if self.send(neighbour, topic, data):
                sent += 1
        return sent

    def subscribe(self, topic, handler):
        self._subscriptions[topic] = handler

    def unsubscribe(self, topic):
        self._subscriptions.pop(topic, None)

    def neighbors(self):
        return self.node.почва.соседи()

    def status(self):
        return self.node.статус()

    def hibernate(self):
        self._stop.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        return self.node.зимовать()

    # ---------- LOOP ----------

    def loop(self, blocking=True, breathe_every=20):
        """
        Main loop: receive + periodic breathe + dispatch.
        """
        def _loop():
            while not self._stop.is_set():
                try:
                    sok = self.node.принять(ждать_сек=0.1)
                    if sok:
                        self._dispatch(sok)
                        self._breath_counter = 0
                    else:
                        self._breath_counter += 1
                        if self._breath_counter >= breathe_every:
                            self.node.дышать()
                            self._breath_counter = 0
                except Exception as e:
                    print('[bridge] loop error: ' + str(e))
                    time.sleep(0.1)

        if blocking:
            _loop()
        else:
            self._thread = threading.Thread(target=_loop, daemon=True)
            self._thread.start()
            return self._thread

    def _dispatch(self, sok):
        from_who, packet = sok
        data = packet.get('данные') or {}

        for _ in range(4):
            if not isinstance(data, dict):
                break
            if data.get('bridge'):
                break
            inner = data.get('данные')
            if isinstance(inner, dict):
                data = inner
            else:
                break

        if not isinstance(data, dict) or not data.get('bridge'):
            return

        topic = data.get('topic')
        if not topic:
            return

        handler = self._subscriptions.get(topic)
        if handler is None:
            return

        try:
            handler(data.get('payload'), data.get('from', from_who))
        except Exception as e:
            print('[bridge] handler error "' + topic + '": ' + str(e))