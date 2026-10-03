"""CLI: python -m inevio_mycorizanet {info|demo}"""
import argparse
import json
import time

from . import create_overlay, __version__
from .transport import UDPTransport, DNSTransport


def main():
    p = argparse.ArgumentParser(prog='inevio_mycorizanet')
    sub = p.add_subparsers(dest='cmd')

    sub.add_parser('info', help='Информация')
    sub.add_parser('demo', help='Демо')

    a = p.parse_args()

    if a.cmd == 'info':
        print('inevio-mycorizanet v' + __version__)
        print('МИКОРИЗАnet — живой overlay-организм')
        print()
        print('Шесть биопринципов:')
        print('  1. Адресация — свой корень .spore')
        print('  2. Мембрана — антигены + потенциал')
        print('  3. Феромоны — маршруты растут сами')
        print('  4. Симбиоз — взаимная выгода')
        print('  5. Кворум — концентрация сигналов')
        print('  6. Осмос — градиент нагрузки')
        print()
        print('Транспорт — автономный выбор (UDP, TCP, DNS, ICMP, HTTP)')

    elif a.cmd == 'demo':
        print('[demo] Создаём overlay...')
        ov = create_overlay('demo-node', secret=b'demo-secret')
        ov.add_peer('demo-peer')

        print('[demo] Отправляем пакет...')
        result = ov.send('demo-peer', b'hello')
        print('[demo] Результат:', result)

        time.sleep(1)
        print()
        print('[demo] Статистика:')
        print(json.dumps(ov.stats(), indent=2, ensure_ascii=False, default=str))

        ov.stop()

    else:
        p.print_help()


if __name__ == '__main__':
    main()