"""NetworkRecon: nslookup/tracert/arp (Win) и dig/tracepath/ip (Linux)."""
import platform, re, subprocess, time
__version__ = "1.0.0"
_IS_WIN = platform.system() == "Windows"

def _run(cmd, timeout=6.0):
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout,
                           encoding="utf-8", errors="replace")
        return r.stdout or ""
    except Exception:
        return ""

def dns_servers(host="example.com", timeout=6.0):
    out = {"servers": [], "type": "unknown", "ok": False}
    if _IS_WIN:
        txt = _run(["nslookup", host], timeout)
    else:
        txt = _run(["dig", "+short", host], timeout)
    servers = list(dict.fromkeys(re.findall(r"(\d+\.\d+\.\d+\.\d+)", txt)))
    out["servers"] = servers[:3]
    if servers:
        if any(s.startswith(("8.8.", "1.1.", "9.9.")) for s in servers):
            out["type"] = "public"
        elif any(s.startswith(("192.168.", "10.", "172.")) for s in servers):
            out["type"] = "local-resolver"
        else:
            out["type"] = "isp-resolver"
        out["ok"] = True
    return out

def route_trace(target="8.8.8.8", max_hops=5, timeout=15.0):
    out = {"hops": [], "depth": 0, "ok": False}
    if _IS_WIN:
        txt = _run(["tracert", "-d", "-h", str(max_hops), "-w", "800", target], timeout)
    else:
        txt = _run(["tracepath", "-m", str(max_hops), target], timeout) or \
              _run(["traceroute", "-n", "-m", str(max_hops), target], timeout)
    hops = re.findall(r"(\d+\.\d+\.\d+\.\d+)", txt)
    out.update(hops=hops, depth=len(hops), ok=bool(hops))
    return out

ISP_TOKENS = ("mts", "beeline", "megafon", "tele2", "rostelecom", "rt.ru", "mgts",
              "ertelecom", "dom.ru", "t2", "yota", "comcast", "verizon", "vodafone",
              "orange", "kpn", "fastweb", "swisscom")

def identify_isp(timeout=15.0):
    if _IS_WIN:
        txt = _run(["tracert", "-h", "3", "-w", "800", "8.8.8.8"], timeout).lower()
    else:
        txt = _run(["traceroute", "-m", "3", "8.8.8.8"], timeout).lower()
    for t in ISP_TOKENS:
        if t in txt:
            return t
    return "unknown"

def neighbors_estimate(timeout=5.0):
    if _IS_WIN:
        txt = _run(["arp", "-a"], timeout)
    else:
        txt = _run(["ip", "neigh"], timeout) or _run(["arp", "-a"], timeout)
    return len(re.findall(r"([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}", txt))

def classify(ssid, dns_list, hops):
    s = (ssid or "").lower(); dns_list = dns_list or []
    if any(k in s for k in ("5g", "lte", "mts", "beeline", "megafon", "tele2")):
        return "cellular-router"
    if any(k in s for k in ("guest", "public", "free", "cafe", "mcdonald")):
        return "public-hotspot"
    if any(k in s for k in ("iot", "smart", "sensor", "home")):
        return "iot-mesh"
    if any(k in s for k in ("corp", "office", "vpn", "work")):
        return "corporate"
    if "8.8.8.8" in dns_list or "1.1.1.1" in dns_list:
        return "consumer-router"
    if hops and hops <= 2:
        return "direct-isp"
    if hops and hops >= 6:
        return "deep-infra"
    return "unknown"

def full_recon(ssid="", bssid="", timeout=6.0):
    """Точка входа: полная разведка. Выход: dict findings."""
    t0 = time.time()
    dns = dns_servers(timeout=timeout)
    trace = route_trace(timeout=timeout * 2)
    isp = identify_isp(timeout=timeout * 2) if trace["ok"] else "unknown"
    return {"ssid": ssid, "bssid": bssid, "dns_servers": dns["servers"],
            "dns_type": dns["type"], "route_hops": trace["hops"],
            "depth": trace["depth"], "isp": isp,
            "neighbors_estimate": neighbors_estimate(),
            "infra_type": classify(ssid, dns["servers"], trace["depth"]),
            "recon_at": time.time(),
            "duration_ms": round((time.time() - t0) * 1000, 1)}

class NetworkRecon:
    dns_servers = staticmethod(dns_servers)
    route_trace = staticmethod(route_trace)
    identify_isp = staticmethod(identify_isp)
    neighbors_estimate = staticmethod(neighbors_estimate)
    full_recon = staticmethod(full_recon)
    classify = staticmethod(classify)
