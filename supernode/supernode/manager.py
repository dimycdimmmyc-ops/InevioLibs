"""SuperNode manager: обученный узел становится учителем сети."""
import json, os, threading, time
__version__ = "1.0.0"
DEFAULTS = {"fitness_threshold": 0.9, "delivery_rate": 0.9,
            "delivery_attempts": 5, "seen_count": 10}

class SuperNodeManager:
    def __init__(self, state_file=None, **criteria):
        self.criteria = dict(DEFAULTS); self.criteria.update(criteria)
        self.state_file = state_file
        self._lock = threading.RLock()
        self.super_nodes = {}
        self._last_broadcast = {}
        self.applied = []
        if state_file and os.path.exists(state_file):
            self.load()

    # ---- ТОЧКИ ВХОДА ----
    def evaluate(self, node, evolution_stats=None, delivery_stats=None):
        """Вход: узел + статистики. Выход: причина повышения или None."""
        evolution_stats = evolution_stats or {}
        delivery_stats = delivery_stats or {}
        c = self.criteria
        fitness = float(evolution_stats.get("best_fitness", 0.0))
        if fitness < c["fitness_threshold"]:
            return None
        ssid = node.get("name", "")
        ds = delivery_stats.get(ssid, {})
        tried = ds.get("tried", []); ok = ds.get("succeeded", [])
        if len(tried) < c["delivery_attempts"]:
            return None
        rate = len(ok) / float(len(tried)) if tried else 0.0
        if rate < c["delivery_rate"]:
            return None
        if node.get("seen_count", 0) < c["seen_count"]:
            return None
        return "fitness=%.3f, delivery=%.0f%% (%d/%d), seen=%d" % (
            fitness, rate * 100, len(ok), len(tried), node.get("seen_count", 0))

    def promote(self, node, evolution_stats=None, delivery_stats=None):
        """Вход: узел. Выход: bool (повышен ли)."""
        nid = node.get("node_id")
        if not nid:
            return False
        with self._lock:
            if nid in self.super_nodes:
                return True
            reason = self.evaluate(node, evolution_stats, delivery_stats)
            if not reason:
                return False
            self.super_nodes[nid] = {
                "node_id": nid, "name": node.get("name"), "type": node.get("type"),
                "promoted_at": time.time(), "reason": reason,
                "experience": {
                    "best_fitness": (evolution_stats or {}).get("best_fitness"),
                    "best_genome": (evolution_stats or {}).get("best_genome"),
                    "best_protocol": (delivery_stats or {}).get(
                        node.get("name"), {}).get("last_method"),
                    "node_type": node.get("type"), "extracted_at": time.time()}}
            if self.state_file:
                self.save()
            return True

    def demote(self, node_id):
        with self._lock:
            return self.super_nodes.pop(node_id, None) is not None

    def apply_experience(self, packet):
        """Вход: пакет опыта от супер-узла сети. Выход: применённая запись."""
        rec = {"from": packet.get("from"), "ts": time.time(),
               "experience": packet.get("experience")}
        with self._lock:
            self.applied.append(rec)
            self.applied = self.applied[-100:]
        return rec

    def broadcast_payload(self, node_id, interval=60.0):
        """Выход: пакет опыта для рассылки соседям (или None)."""
        with self._lock:
            sn = self.super_nodes.get(node_id)
            if not sn:
                return None
            now = time.time()
            if now - self._last_broadcast.get(node_id, 0) < interval:
                return None
            self._last_broadcast[node_id] = now
            return {"type": "super_experience", "from": node_id,
                    "from_name": sn.get("name"),
                    "experience": sn.get("experience"), "ts": now}

    # ---- ТОЧКИ ВЫХОДА ----
    def is_super(self, node_id):
        with self._lock:
            return node_id in self.super_nodes

    def get_all(self):
        with self._lock:
            return dict(self.super_nodes)

    def get_stats(self):
        with self._lock:
            return {"count": len(self.super_nodes),
                    "applied_experience": len(self.applied),
                    "nodes": [{"node_id": k, "name": v.get("name"),
                               "type": v.get("type"), "reason": v.get("reason"),
                               "promoted_at": v.get("promoted_at")}
                              for k, v in self.super_nodes.items()]}

    def save(self):
        if not self.state_file:
            return
        try:
            os.makedirs(os.path.dirname(self.state_file) or ".", exist_ok=True)
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(self.super_nodes, f, ensure_ascii=False)
        except OSError:
            pass

    def load(self):
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                self.super_nodes.update(json.load(f))
        except (OSError, ValueError):
            pass
