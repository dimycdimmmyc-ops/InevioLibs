"""BREATHE — адаптивный heartbeat."""
from ..constants import HEARTBEAT_MIN, HEARTBEAT_MAX


def breathe(mycelium, found_count):
    """Адаптивный sleep: быстрее при активности."""
    if found_count > 0:
        mycelium._load = min(1.0, mycelium._load + 0.3)
    else:
        mycelium._load = max(0.0, mycelium._load - 0.1)

    base = HEARTBEAT_MAX - int(mycelium._load * (HEARTBEAT_MAX - HEARTBEAT_MIN))
    return max(HEARTBEAT_MIN, base)