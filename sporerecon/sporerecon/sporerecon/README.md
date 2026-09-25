# Пакет sporerecon (импортируемый модуль)
recon.py    — NetworkRecon: full_recon / dns_servers / route_trace /
              identify_isp / neighbors_estimate / _classify.
server.py   — REST-надстройка (stdlib): server.main(host, port=8702).
__main__.py — CLI: python -m sporerecon [SSID BSSID] | --serve.
Импорт: from sporerecon import NetworkRecon
