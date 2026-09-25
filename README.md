# InevioLibs — живая сеть для автономных устройств

Экосистема из шести пакетов.

## Компоненты

| Пакет | Назначение | PyPI |
|---|---|---|
| **spore-net** | Живая сеть: 8 почв, дыхание, зимовка | [pypi](https://pypi.org/project/spore-net/) |
| **spore-bridge** | Единый мост | [pypi](https://pypi.org/project/spore-bridge/) |
| **supernode** | Коллективное обучение | [pypi](https://pypi.org/project/supernode/) |
| **sporerecon** | Пассивная разведка | [pypi](https://pypi.org/project/sporerecon/) |
| **inevio-stealth** | Адаптивная маскировка | — |
| **inevio-mycelium** | Живая грибница: поиск, закрепление, проникновение вглубь | — |

## Установка

    pip install inevio-ecosystem

## Быстрый старт

    from spore_bridge import SporeBridge
    from inevio_mycelium import Mycelium

    bridge = SporeBridge('node-1', port=8700)
    bridge.loop(blocking=False)

    org = Mycelium(bridge, max_depth=10)
    org.start()

    print(org.get_stats())
    # {'attached': 42, 'depth_max': 5, ...}

## Архитектура

    supernode  sporerecon  inevio-stealth  inevio-mycelium
        │          │             │                │
        └──────────┼─────────────┼────────────────┘
                   │             │
                   ▼             ▼
              spore-bridge ──────┘
                   │
                   ▼
              spore-net
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
     UDP      Wi-Fi Direct    BLE

## Лицензия

MIT