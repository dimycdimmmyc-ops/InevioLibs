"""МИКОРИЗАnet · Уровень 1 — Адресация: свой DNS-корень .spore."""
import hashlib
import json
import os
import socket
import threading
import time

from .constants import TLD


def name_for(node_id):
    return hashlib.sha1(("name:" + node_id).encode()).hexdigest()[:16] + "." + TLD


def ula_for(node_id):
    h = hashlib.sha1(("addr:" + node_id).encode()).digest()
    gid = h[0:10].hex()
    iid = h[10:18].hex()
    return "fd%s:%s:%s:%s:%s:%s:%s:%s" % (
        gid[0:2], gid[2:6], gid[6:10],
        iid[0:4], iid[4:8], iid[8:12], iid[12:16], "0001")


class SporeAddressing:
    """Свой DNS-корень .spore + детерминированные ULA."""

    def __init__(self, zone_file=None):
        self.zone_file = zone_file
        self._lock = threading.RLock()
        self._zone = {}
        self._srv = None
        self._stop = None
        self._load()

    def register(self, node_id, pubkey_fp=""):
        with self._lock:
            rec = self._zone.get(node_id)
            if rec is None:
                rec = {
                    "name": name_for(node_id),
                    "address": ula_for(node_id),
                    "pubkey_fp": pubkey_fp,
                    "registered_at": time.time(),
                }
                self._zone[node_id] = rec
                self._save()
            return dict(rec)

    def resolve(self, name):
        with self._lock:
            for nid, rec in self._zone.items():
                if rec["name"] == name:
                    return dict(rec, node_id=nid)
        return None

    def resolve_node(self, node_id):
        with self._lock:
            rec = self._zone.get(node_id)
            return dict(rec, node_id=node_id) if rec else None

    def reverse(self, address):
        with self._lock:
            for nid, rec in self._zone.items():
                if rec["address"] == address:
                    return dict(rec, node_id=nid)
        return None

    def records(self):
        with self._lock:
            return [dict(r, node_id=n) for n, r in self._zone.items()]

    def _save(self):
        if not self.zone_file:
            return
        try:
            os.makedirs(os.path.dirname(self.zone_file) or ".", exist_ok=True)
            with open(self.zone_file, "w", encoding="utf-8") as f:
                json.dump(self._zone, f, ensure_ascii=False)
        except OSError:
            pass

    def _load(self):
        if self.zone_file and os.path.exists(self.zone_file):
            try:
                with open(self.zone_file, "r", encoding="utf-8") as f:
                    self._zone = json.load(f)
            except (OSError, ValueError):
                self._zone = {}

    def start_service(self, host="127.0.0.1", port=5353):
        if self._srv:
            return
        self._srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._srv.bind((host, port))
        self._srv.settimeout(0.5)
        self._stop = threading.Event()

        def loop():
            while not self._stop.is_set():
                try:
                    data, addr = self._srv.recvfrom(2048)
                    q = (json.loads(data.decode("utf-8")) or {}).get("q", "")
                    rec = self.resolve(q)
                    self._srv.sendto(json.dumps({
                        "a": rec["address"] if rec else None,
                        "name": rec["name"] if rec else None,
                    }).encode(), addr)
                except socket.timeout:
                    continue
                except Exception:
                    continue
        threading.Thread(target=loop, daemon=True).start()

    def stop_service(self):
        if self._stop:
            self._stop.set()
        if self._srv:
            try:
                self._srv.close()
            except Exception:
                pass
            self._srv = None