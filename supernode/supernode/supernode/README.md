# Пакет supernode (импортируемый модуль)
manager.py  — SuperNodeManager: promote / evaluate / apply_experience /
              broadcast_payload / is_super / get_all / get_stats + save/load (JSON).
server.py   — REST-надстройка над manager (stdlib): server.main(host, port=8701).
__main__.py — CLI-точка входа: python -m supernode {serve|stats|promote}.
Импорт: from supernode import SuperNodeManager
