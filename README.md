# InevioLibs — живая сеть для автономных устройств

Экосистема из пяти пакетов: транспорт, мост, обучение,
разведка, маскировка. Работает без интернета, сервера,
администратора. Только stdlib Python.

## Компоненты

| Пакет | Назначение | PyPI | GitHub |
|---|---|---|---|
| **spore-net** | Живая сеть: 8 адаптеров транспорта, дыхание, зимовка | [pypi](https://pypi.org/project/spore-net/) | [→](spore-net/) |
| **spore-bridge** | Единый мост между библиотеками | [pypi](https://pypi.org/project/spore-bridge/) | [→](spore-bridge/) |
| **supernode** | Коллективное обучение через гифы | [pypi](https://pypi.org/project/supernode/) | [→](supernode/) |
| **sporerecon** | Пассивная разведка сети | [pypi](https://pypi.org/project/sporerecon/) | [→](sporerecon/) |
| **inevio-stealth** | Адаптивная маскировка | [pypi](https://pypi.org/project/inevio-stealth/) | [→](inevio-stealth/) |

## Установка

Всё одной командой:

    pip install inevio-ecosystem

Или по отдельности:

    pip install spore-net
    pip install spore-bridge
    pip install supernode
    pip install sporerecon
    pip install inevio-stealth

## Быстрый старт

    from spore_bridge import SporeBridge
    from spore.soil import ПочваSocket

    bridge = SporeBridge('my-node', port=8700)
    bridge.loop(blocking=False)

    from supernode import SuperNodeManager, attach_bridge
    from sporerecon import attach_bridge as recon_attach
    from stealth import attach_bridge as stealth_attach

    manager = SuperNodeManager()
    attach_bridge(manager, bridge)

## Сборка и установка

    .\build_all.ps1              # тесты + wheel в dist\
    .\build_all.ps1 -Exe         # + standalone .exe
    .\build_all.ps1 -SkipTests   # только сборка
    .\install_all.ps1            # установка всех wheel

## Тесты

    cd supernode  ; python -m unittest discover -s tests -v
    cd sporerecon ; python -m unittest discover -s tests -v
    cd stealth    ; python -m unittest discover -s tests -v

## REST-порты

    supernode     -> http://127.0.0.1:8701
    sporerecon    -> http://127.0.0.1:8702
    stealth       -> http://127.0.0.1:8704  (приёмник фрагментов: 8703)

## Архитектура

    supernode    sporerecon    inevio-stealth
        │            │              │
        └────────────┼──────────────┘
                     │
                     ▼
              spore-bridge
                     │
                     ▼
                spore-net
                     │
       ┌─────────────┼─────────────┐
       │             │             │
       ▼             ▼             ▼
    UDP        Wi-Fi Direct      BLE
                           (+ 5 других почв)

## Где применяется

- **spore-net** — транспорт для любого P2P, mesh, IoT
- **supernode** — роевая робототехника, federated learning, V2X
- **sporerecon** — инвентаризация сетей, red-team, антифрод
- **inevio-stealth** — privacy-инструменты, исследование covert-каналов
- **FPV-дроны** — обход РЭБ через mesh

## Лицензирование (Dual Licensing)

- **Сообщество:** AGPL-3.0 (файл [LICENSE](LICENSE))
- **Бизнес:** коммерческая лицензия (файл [LICENSE-COMMERCIAL.md](LICENSE-COMMERCIAL.md))
- **Copyright (c) 2026 dimon027081**