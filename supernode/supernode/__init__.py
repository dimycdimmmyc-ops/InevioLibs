"""SuperNode: коллективное обучение mesh-сетей.
Точки входа: promote(), evaluate(), apply_experience(), broadcast_payload(), CLI, REST.
Точки выхода: get_stats(), get_all(), broadcast_payload() -> dict, state-file JSON."""
from .manager import SuperNodeManager, DEFAULTS, __version__
__all__ = ["SuperNodeManager", "DEFAULTS", "__version__"]
