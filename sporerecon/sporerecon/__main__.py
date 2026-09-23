"""CLI: python -m sporerecon [SSID BSSID] | --serve"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sporerecon.recon import full_recon

def main():
    p = argparse.ArgumentParser(prog="sporerecon")
    p.add_argument("ssid", nargs="?", default="")
    p.add_argument("bssid", nargs="?", default="")
    p.add_argument("--serve", action="store_true")
    p.add_argument("--port", type=int, default=8702)
    a = p.parse_args()
    if a.serve:
        from sporerecon.server import main as serve
        serve(port=a.port)
    else:
        print(json.dumps(full_recon(a.ssid, a.bssid), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
