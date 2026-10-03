"""МИКОРИЗАnet — overlay-организм (главный класс)."""
import threading
import time

from .addressing import SporeAddressing
from .membrane import Membrane
from .trails import TrailTable
from .symbiosis import SymbiosisLedger
from .quorum import QuorumSensor
from .osmosis import OsmoticBalancer
from .immune import ImmuneMemory
from .transport import TransportSelector
from .constants import TICK_INTERVAL


class MycorrhizaOverlay:
    """Живой overlay-организм МИКОРИЗАnet."""

    def __init__(self, self_id, secret, zone_file=None,
                 transports=None, tick_interval=TICK_INTERVAL):
        self.self_id = self_id
        self.addressing = SporeAddressing(zone_file=zone_file)
        self.membrane = Membrane(secret, self_id)
        self.trails = TrailTable()
        self.symbiosis = SymbiosisLedger()
        self.quorum = QuorumSensor()
        self.osmosis = OsmoticBalancer()
        self.immune = ImmuneMemory()
        self.selector = TransportSelector(transports or [])

        self.immune.learn_self(self_id)
        self.addressing.register(self_id)

        self._peers = {}
        self._lock = threading.RLock()
        self._last_tick = time.time()
        self._tick_interval = tick_interval
        self._tick_thread = None
        self._stop = None

    # ---------- Жизненный цикл ----------

    def tick(self):
        now = time.time()
        dt = now - self._last_tick
        self._last_tick = now
        self.trails.evaporate(dt)
        self.quorum.tick(dt)
        self.immune.decay_tick(dt)
        self.symbiosis.prune(now)
        self.selector.tick(dt)
        self.flush_buffer()

    def start(self):
        if self._tick_thread:
            return
        self._stop = threading.Event()

        def loop():
            while not self._stop.is_set():
                try:
                    self.tick()
                except Exception:
                    pass
                self._stop.wait(self._tick_interval)
        self._tick_thread = threading.Thread(target=loop, daemon=True)
        self._tick_thread.start()

    def stop(self):
        if self._stop:
            self._stop.set()
        self.addressing.stop_service()

    def start_resolver(self, port=5353):
        self.addressing.start_service(port=port)

    # ---------- Пиры ----------

    def add_peer(self, node_id, pubkey_fp=""):
        with self._lock:
            rec = self.addressing.register(node_id, pubkey_fp)
            self._peers[node_id] = rec
        return rec

    def peers(self):
        with self._lock:
            return dict(self._peers)

    # ---------- Отправка / приём ----------

    def send(self, dest, payload, task=None):
        if self.immune.blocked(dest):
            return {"status": "blocked", "dest": dest}

        hop = self.trails.choose(dest)
        if not hop and dest in self._peers:
            hop = dest
        if not hop:
            hop = self.osmosis.downhill(exclude=(self.self_id,))
        if not hop:
            if isinstance(payload, bytes):
                self.osmosis.accept((dest, payload, time.time()))
            return {"status": "buffered", "dest": dest}

        blob = self.membrane.seal(
            payload if isinstance(payload, bytes) else str(payload).encode("utf-8"),
            hop)

        rec = self.peers().get(hop)
        if not rec:
            return {"status": "no_peer", "hop": hop}

        host = "127.0.0.1"
        port = 8700

        result = self.selector.send(host, port, blob, task=task)
        if result.get("status") == "sent":
            self.symbiosis.record_given(hop)
            self.membrane.charge(self.self_id, +0.01)
        else:
            self.fail(dest, hop)
        return result

    def receive(self, src, blob):
        if self.immune.blocked(src):
            return {"status": "blocked", "src": src}
        if not self.membrane.verify(blob, src):
            self.immune.attack(src, 1.0)
            return {"status": "foreign", "src": src}
        payload = self.membrane.payload(blob)
        self.symbiosis.record_received(src)
        self.quorum.signal("traffic")
        self.membrane.charge(src, -0.01)
        return {"status": "own", "src": src, "payload": payload}

    # ---------- Обучение ----------

    def ack(self, dest, hop, rtt=None):
        self.trails.deposit(dest, hop, rtt=rtt)
        self.quorum.signal("delivery")
        self.membrane.charge(hop, +0.02)

    def fail(self, dest, hop):
        self.trails.penalize(dest, hop)
        self.immune.attack(hop, 0.5)
        self.membrane.charge(hop, -0.05)

    def flush_buffer(self):
        for dest, payload, ts in self.osmosis.drain():
            if time.time() - ts > 300:
                continue
            self.send(dest, payload)

    # ---------- Сводка ----------

    def stats(self):
        return {
            "self": self.self_id,
            "peers": len(self._peers),
            "zone": len(self.addressing.records()),
            "trails": self.trails.snapshot(),
            "symbiosis": self.symbiosis.snapshot(),
            "quorum": self.quorum.concentrations(),
            "osmosis": {
                "load": self.osmosis.load,
                "pressure": round(self.osmosis.pressure(), 3),
            },
            "immune": self.immune.stats(),
            "transport": self.selector.stats(),
        }