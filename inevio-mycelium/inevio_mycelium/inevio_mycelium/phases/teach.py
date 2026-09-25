"""TEACH — передача знания другим грибницам."""
import time
from ..constants import TOPIC_MAP


def teach(mycelium):
    """Передать карту другим."""
    if not mycelium.memory.has_new_since_teach():
        return False

    my_map = {
        'from': mycelium.env.name,
        'ts': time.time(),
        'nodes': mycelium.memory.get_recent_nodes(limit=100),
        'depth_max': mycelium.memory.max_depth(),
    }

    sent = mycelium.env.broadcast(TOPIC_MAP, my_map)
    mycelium.stats.inc('maps_taught')
    mycelium.memory.mark_taught()
    mycelium.memory.log_phase('teach', 0, 'nodes=' + str(len(my_map['nodes'])))

    return sent > 0