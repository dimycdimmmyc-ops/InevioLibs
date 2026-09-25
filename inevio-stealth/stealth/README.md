# Пакет stealth (импортируемый модуль)
engine.py   — StealthEngine (send/probe/get_stats/get_channels + state),
              StealthListener (приём фрагментов, messages()),
              BayesianUpdater (бета + UCB1), PolymorphicEncoder (профили каналов).
server.py   — REST-надстройка (stdlib): server.main(host, port=8704).
__main__.py — CLI: python -m stealth {listen|send|probe|stats|serve}.
Импорт: from stealth import StealthEngine, StealthListener
