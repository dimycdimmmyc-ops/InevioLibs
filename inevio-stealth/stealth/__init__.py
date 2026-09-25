"""Stealth: adaptive stealth with spore-net integration."""
__version__ = '1.1.0'

from .engine import (
    StealthEngine,
    StealthListener,
    BayesianUpdater,
    PolymorphicEncoder,
)
from .bridge_attach import attach_bridge, send_via_spore, RECEIVER

__all__ = [
    '__version__',
    'StealthEngine',
    'StealthListener',
    'BayesianUpdater',
    'PolymorphicEncoder',
    'attach_bridge',
    'send_via_spore',
    'RECEIVER',
]