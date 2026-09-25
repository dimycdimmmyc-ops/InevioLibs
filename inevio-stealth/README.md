# stealth — адаптивная скрытность (замкнутый цикл)

## Что это
StealthEngine + StealthListener: замкнутый цикл
«зонд -> маскировка -> отправка -> обучение».
Байесовский апдейтер (бета-распределение + UCB1) копит вероятность успеха
каждого канала; полиморфный энкодер маскирует пакет под профиль канала
(размер, джиттер); слушатель принимает фрагменты и собирает сообщение.

## Для чего
- исследование covert-каналов и DPI/IDS на СВОИХ сетях и стендах
- обход цензуры в легальных сценариях (защита связи журналистов)
- маскировка трафика во враждебной среде: система сама учится, какой канал проходит
- privacy-инструменты: трафик неотличим от фонового
ВНИМАНИЕ dual-use: применять только на своих сетях и при наличии разрешения.

## Структура папки
    stealth\engine.py    — StealthEngine, StealthListener, BayesianUpdater, PolymorphicEncoder
    stealth\server.py    — REST-сервер, порт 8704
    stealth\__main__.py  — CLI: python -m stealth
    tests\               — тесты (включая loopback send->listener)
    setup.py             — сборка wheel

## Как использовать
Python API (точки входа):
    from stealth import StealthEngine, StealthListener
    lis = StealthListener(port=8703) ; lis.serve_forever()   # приёмник
    eng = StealthEngine(state_file="stealth_state.json")
    res = eng.send(b"payload", "127.0.0.1:8703")             # отправка с обучением
    eng.probe("host")                                        # зонд доступности каналов
Точки выхода:
    send -> {success, channel, attempts, latency_ms, fragment_size}
    listener.messages()          -> список собранных сообщений
    eng.get_stats() / get_channels() -> статистика и вероятности каналов
CLI:
    python -m stealth listen --port 8703
    python -m stealth send --target 127.0.0.1:8703 --message "текст"
    python -m stealth probe --target host
    python -m stealth stats --state stealth_state.json
    python -m stealth serve --port 8704
REST (любой язык):
    POST /send {payload, target}   POST /probe {target}
    GET  /stats                    GET  /channels
Сборка / тесты:
    python -m pip wheel . --no-deps -w ..\dist
    python -m unittest discover -s tests -v
