"""CLI: python -m spore_bridge {info|echo}"""
import argparse
import json
import time

from .bridge import SporeBridge


def main():
    p = argparse.ArgumentParser(prog='spore_bridge')
    sub = p.add_subparsers(dest='cmd')

    s = sub.add_parser('info')
    s.add_argument('--name', default='bridge')
    s.add_argument('--port', type=int, default=8700)

    s = sub.add_parser('echo')
    s.add_argument('--name', default='bridge')
    s.add_argument('--port', type=int, default=8700)

    a = p.parse_args()

    if a.cmd == 'info':
        bridge = SporeBridge(a.name, port=a.port)
        print(json.dumps(bridge.статус(), ensure_ascii=False, indent=2))
        bridge.зимовать()

    elif a.cmd == 'echo':
        bridge = SporeBridge(a.name, port=a.port)

        def эхо(payload, от_кого):
            print(f'[{a.name}] от {от_кого}: {payload}')

        bridge.подписаться('echo', эхо)
        print(f'[{a.name}] слушаю на порту {a.port}, Ctrl+C для выхода')
        try:
            bridge.цикл()
        except KeyboardInterrupt:
            print(f'\n[{a.name}] завершаю...')
            bridge.зимовать()

    else:
        p.print_help()


if __name__ == '__main__':
    main()