# supernode — коллективное обучение сетевых узлов

## Что это
SuperNodeManager: повышает узел до статуса «супер-узел» по формальным критериям
(fitness, доля успешных доставок, число попыток, стабильность) и хранит его
«пакет опыта» для передачи другим узлам. Без центрального сервера.

## Для чего
- mesh/IoT-сети: обученные узлы учат новичков, сеть сходится быстрее
- роевая робототехника и federated learning: передача лучших параметров без центра
- любое распределённое приложение, где «сильный учит слабого»
- ВНЕ InevioNet: работает автономно, зависимости только stdlib

## Структура папки
    supernode\manager.py   — вся логика (SuperNodeManager)
    supernode\server.py    — REST-сервер (stdlib http.server), порт 8701
    supernode\__main__.py  — CLI: python -m supernode
    tests\                 — тесты
    setup.py               — сборка wheel

## Как использовать
Python API (точки входа):
    from supernode import SuperNodeManager
    m = SuperNodeManager(fitness_threshold=0.9, delivery_rate_threshold=0.9,
                         delivery_attempts_threshold=5, seen_count_threshold=10)
    ok  = m.promote(node, evolution_stats, delivery_stats)  # вход: повысить узел
    m.apply_experience(packet)                             # вход: применить чужой опыт
Точки выхода:
    m.broadcast_payload(node_id, interval=60)  -> dict пакета опыта или None
    m.get_stats() / m.get_all()                -> dict состояния
    состояние переживает рестарт через state_file (JSON)
CLI:
    python -m supernode serve --port 8701
    python -m supernode stats --state state.json
    python -m supernode promote --node node.json --evo evo.json --delivery del.json
REST (любой язык):
    GET  /stats            POST /promote {node, evolution_stats, delivery_stats}
    POST /apply {from, experience}        POST /broadcast {node_id, interval}
Сборка / тесты:
    python -m pip wheel . --no-deps -w ..\dist
    python -m unittest discover -s tests -v
