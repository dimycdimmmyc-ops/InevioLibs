"""Mycelium — живая грибница.

Растёт вглубь через сеть:
  scout → attach → penetrate → assess → teach → merge → breathe
"""
import time
import threading

from .constants import (
    MAX_DEPTH_DEFAULT, TOPIC_HELLO, TOPIC_MAP,
    TOPIC_REQUEST_MAP, TOPIC_PENETRATE,
    HEARTBEAT_BASE, BATCH_ATTACH,
)
from .memory import MyceliumMemory
from .stats import MyceliumStats
from . import phases


class Mycelium:
    """Живая грибница для Inevio."""

    def __init__(self, env, max_depth=MAX_DEPTH_DEFAULT, auto_start=False):
        self.env = env
        self.max_depth = max_depth
        self.running = False
        self._load = 0.0
        self._lock = threading.Lock()

        self.memory = MyceliumMemory()
        self.stats = MyceliumStats()

        # Подписываемся на топики
        self._setup_subscriptions()

        if auto_start:
            self.start()

    def _setup_subscriptions(self):
        """Подписки на входящие топики."""
        self.env.subscribe(TOPIC_HELLO, self._on_hello)
        self.env.subscribe(TOPIC_MAP, self._on_map)
        self.env.subscribe(TOPIC_REQUEST_MAP, self._on_request_map)

    def _on_hello(self, data, from_who):
        """Кто-то поздоровался — добавляем."""
        addr = data.get('from', from_who)
        if addr:
            self.memory.add_node(addr, {
                'addr': addr, 'type': 'inevionet',
                'depth': data.get('depth', 1), 'source': 'hello',
            })

    def _on_map(self, data, from_who):
        """Пришла карта — merge."""
        added = phases.merge(self, data)
        if added:
            self.env.log('info', '[Mycelium] merge: +' + str(added))

    def _on_request_map(self, data, from_who):
        """Просят карту — отдаём."""
        requester = data.get('from', from_who)
        if not requester:
            return
        my_map = {
            'from': self.env.name,
            'ts': time.time(),
            'nodes': self.memory.get_recent_nodes(limit=100),
            'depth_max': self.memory.max_depth(),
        }
        self.env.send(requester, TOPIC_MAP, my_map)

    # ==========================================================
    # Lifecycle
    # ==========================================================

    def start(self):
        if self.running:
            return
        self.running = True
        threading.Thread(
            target=self._live, daemon=True, name='mycelium'
        ).start()
        self.env.log('info', '[Mycelium] started (depth_max=' + str(self.max_depth) + ')')

    def stop(self):
        self.running = False

    def _live(self):
        """Главный цикл."""
        time.sleep(10)
        while self.running:
            try:
                t0 = time.time()

                # ПОИСК
                found = phases.scout(self)

                # ОЦЕНКА + ЗАКРЕПЛЕНИЕ
                attached = 0
                for node in found[:BATCH_ATTACH]:
                    plan = phases.assess(self, node)
                    if plan.get('action') in ('attach', 'penetrate'):
                        if phases.attach(self, node):
                            attached += 1

                # ПРОНИКНОВЕНИЕ ВГЛУБЬ
                penetrated = phases.penetrate(self)

                # ОБУЧЕНИЕ
                phases.teach(self)

                # Статистика
                self.stats.inc('cycles')
                depth = self.memory.max_depth()
                if depth > self.stats.get('max_depth', 0):
                    self.stats.set('max_depth', depth)

                # АДАПТИВНЫЙ HEARTBEAT
                sleep = phases.breathe(self, len(found))

                elapsed = time.time() - t0
                self.env.log('info',
                    '[Mycelium] cycle=' + str(self.stats.get('cycles')) +
                    ' found=' + str(len(found)) +
                    ' attached=' + str(attached) +
                    ' penetrated=' + str(penetrated) +
                    ' depth=' + str(depth) +
                    ' elapsed=' + str(round(elapsed, 1)) + 's' +
                    ' sleep=' + str(sleep) + 's'
                )

                time.sleep(sleep)
            except Exception as e:
                self.env.log('error', '[Mycelium] cycle: ' + str(e))
                time.sleep(5)

        self.env.log('info', '[Mycelium] stopped')

    # ==========================================================
    # Public API
    # ==========================================================

    def get_stats(self):
        out = self.stats.to_dict()
        mem = self.memory.get_stats()
        out.update({
            'running': self.running,
            'load': self._load,
            'max_depth_limit': self.max_depth,
            'nodes_in_memory': mem['nodes'],
            'attached': mem['attached'],
            'depth_max': mem['depth_max'],
        })
        return out

    def get_phase_log(self, n=30):
        return self.memory.get_phase_log(n)

    def __repr__(self):
        return 'Mycelium(cycles=' + str(self.stats.get('cycles')) + \
               ', nodes=' + str(len(self.memory.nodes)) + ')'