"""CLI: python -m stealth {listen|send|probe|stats}"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from stealth.engine import StealthEngine, StealthListener

def main():
    p = argparse.ArgumentParser(prog="stealth")
    sub = p.add_subparsers(dest="cmd")
    s = sub.add_parser("listen"); s.add_argument("--port", type=int, default=8703)
    s = sub.add_parser("send"); s.add_argument("--target", required=True)
    s.add_argument("--message", required=True); s.add_argument("--state", default=None)
    s = sub.add_parser("probe"); s.add_argument("--target", required=True)
    s = sub.add_parser("stats"); s.add_argument("--state", default=None)
    a = p.parse_args()
    if a.cmd == "listen":
        StealthListener.main(port=a.port)
    elif a.cmd == "send":
        print(json.dumps(StealthEngine(state_file=a.state).send(a.message, a.target),
                         ensure_ascii=False))
    elif a.cmd == "probe":
        print(json.dumps(StealthEngine(state_file=a.state).probe(a.target),
                         ensure_ascii=False))
    elif a.cmd == "stats":
        print(json.dumps(StealthEngine(state_file=a.state).get_stats(), indent=2))
    else:
        p.print_help()

if __name__ == "__main__":
    main()
