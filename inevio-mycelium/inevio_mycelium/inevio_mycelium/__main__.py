"""CLI: python -m inevio_mycelium {info|demo}"""
import argparse
import json
import threading
import time

from .organism import Mycelium
from .env_mock import EnvMock


def main():
    p = argparse.ArgumentParser(prog='inevio_mycelium')
    sub = p.add_subparsers(dest='cmd')

    sub.add_parser('info', help='Информация о пакете')
    sub.add_parser('demo', help='Демо с mock-средой')

    a = p.parse_args()

    if a.cmd == 'info':
        from . import __version__
        print('inevio-mycelium v' + __version__)
        print('Живая грибница для Inevio')
        print()
        print('Фазы: scout → attach → penetrate → assess → teach → merge')

    elif a.cmd == 'demo':
        print('[demo] Создаём mock-среду...')
        env = EnvMock('demo-node')
        env.add_discover('10.0.0.2')
        env.add_discover('10.0.0.3')
        env.add_discover('10.0.0.4')

        my = Mycelium(env, max_depth=5)

        def run_fast():
            time.sleep(0.5)
            from . import phases
            from .constants import BATCH_ATTACH
            while my.running:
                try:
                    t0 = time.time()
                    found = phases.scout(my)
                    attached = 0
                    for node in found[:BATCH_ATTACH]:
                        plan = phases.assess(my, node)
                        if plan.get('action') in ('attach', 'penetrate'):
                            if phases.attach(my, node):
                                attached += 1
                    penetrated = phases.penetrate(my)
                    phases.teach(my)

                    my.stats.inc('cycles')
                    depth = my.memory.max_depth()
                    if depth > my.stats.get('max_depth', 0):
                        my.stats.set('max_depth', depth)

                    print('[demo] cycle=' + str(my.stats.get('cycles')) +
                          ' found=' + str(len(found)) +
                          ' attached=' + str(attached) +
                          ' penetrated=' + str(penetrated) +
                          ' depth=' + str(depth))

                    # Короткий sleep для демо
                    time.sleep(1.0)
                except Exception as e:
                    print('[demo] error: ' + str(e))
                    time.sleep(1)

        my.running = True
        threading.Thread(target=run_fast, daemon=True).start()

        print('[demo] Запускаем грибницу на 10 секунд...')
        time.sleep(10)
        my.stop()
        time.sleep(0.5)

        print()
        print('[demo] Статистика:')
        print(json.dumps(my.get_stats(), indent=2, ensure_ascii=False))

    else:
        p.print_help()


if __name__ == '__main__':
    main()