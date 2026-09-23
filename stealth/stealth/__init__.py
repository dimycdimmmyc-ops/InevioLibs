"""Stealth: адаптивная скрытность замкнутого цикла (probe -> mask -> send -> learn).
Точки входа: StealthEngine.probe(), .send(), StealthListener.main(), CLI, REST.
Точки выхода: result dict, get_stats(), get_channels(), сообщения слушателя."""
from .engine import (StealthEngine, StealthListener, BayesianUpdater,
                     PolymorphicEncoder, __version__)
__all__ = ["StealthEngine", "StealthListener", "BayesianUpdater",
           "PolymorphicEncoder", "__version__"]
