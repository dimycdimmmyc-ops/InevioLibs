"""CLI: python -m supernode {serve|stats|promote}"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from supernode.manager import SuperNodeManager

def main():
    p = argparse.ArgumentParser(prog="supernode")
    sub = p.add_subparsers(dest="cmd")
    s = sub.add_parser("serve"); s.add_argument("--host", default="127.0.0.1")
    s.add_argument("--port", type=int, default=8701)
    s = sub.add_parser("stats"); s.add_argument("--state", default=None)
    s = sub.add_parser("promote"); s.add_argument("--node", required=True)
    s.add_argument("--evo", default=None); s.add_argument("--delivery", default=None)
    s.add_argument("--state", default=None)
    a = p.parse_args()
    if a.cmd == "serve":
        from supernode.server import main as serve
        serve(a.host, a.port)
    elif a.cmd == "stats":
        print(json.dumps(SuperNodeManager(state_file=a.state).get_stats(),
                         ensure_ascii=False, indent=2))
    elif a.cmd == "promote":
        m = SuperNodeManager(state_file=a.state)
        node = json.load(open(a.node, encoding="utf-8"))
        evo = json.load(open(a.evo, encoding="utf-8")) if a.evo else {}
        dl = json.load(open(a.delivery, encoding="utf-8")) if a.delivery else {}
        print(json.dumps({"promoted": m.promote(node, evo, dl)}, ensure_ascii=False))
    else:
        p.print_help()

if __name__ == "__main__":
    main()
