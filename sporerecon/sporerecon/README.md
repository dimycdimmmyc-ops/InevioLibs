# sporerecon — реальная разведка сети без прав администратора

## Что это
NetworkRecon: собирает РЕАЛЬНЫЕ факты о сети системными утилитами
(nslookup, tracert/tracepath, arp/ip neigh): DNS-резолверы, глубина маршрута
до интернета, ISP по PTR-именам, число соседей в подсети, тип инфраструктуры.

## Для чего
- инвентаризация и аудит сетей: ISP, глубина, тип инфраструктуры, соседи
- red-team разведка без админ-прав и без сканеров вроде Nmap (только легальные сети)
- антифрод: проверка, откуда реально подключён клиент, по DNS/ISP-сигнатурам
- вход для маскировки: тип инфраструктуры -> выбор профиля маскировки
- ВНЕ InevioNet: автономно, stdlib only, Windows + Linux

## Структура папки
    sporerecon\recon.py    — NetworkRecon (вся логика)
    sporerecon\server.py   — REST-сервер, порт 8702
    sporerecon\__main__.py — CLI: python -m sporerecon
    tests\                 — тесты
    setup.py               — сборка wheel

## Как использовать
Python API (точки входа):
    from sporerecon import NetworkRecon
    f = NetworkRecon.full_recon("MyWiFi", "04:ba:d6:a3:58:c5")
    NetworkRecon.dns_servers() / route_trace() / identify_isp() / neighbors_estimate()
Точка выхода — dict findings:
    dns_servers, dns_type, route_hops, depth, isp,
    neighbors_estimate, infra_type, recon_at, duration_ms
    infra_type: cellular-router | public-hotspot | iot-mesh | corporate |
                consumer-router | direct-isp | deep-infra | unknown
CLI:
    python -m sporerecon "SSID" "BSSID"
    python -m sporerecon --serve --port 8702
REST (любой язык):
    GET /recon?ssid=..&bssid=..     GET /neighbors     GET /isp
Сборка / тесты:
    python -m pip wheel . --no-deps -w ..\dist
    python -m unittest discover -s tests -v
