"""SuperNode: коллективное обучение mesh-сетей."""
__version__ = '1.1.0'

from .manager import SuperNodeManager, DEFAULTS
from .bridge_attach import attach_bridge

__all__ = ["SuperNodeManager", "DEFAULTS", "__version__", "attach_bridge"]