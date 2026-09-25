"""PENETRATE — проникновение вглубь через закреплённые узлы."""
import time
from ..constants import TOPIC_REQUEST_MAP, BATCH_PENETRATE


def penetrate(mycelium):
    """Просит карты у закреплённых узлов."""
    requested = 0
    for addr, node in list(mycelium.memory.attached.items()):
        if node.get('asked_map'):
            continue
        if requested >= BATCH_PENETRATE:
            break

        ok = mycelium.env.send(addr, TOPIC_REQUEST_MAP, {
            'from': mycelium.env.name,
            'max_nodes': 100,
            'ts': time.time(),
        })

        if ok:
            node['asked_map'] = True
            requested += 1

    if requested > 0:
        mycelium.stats.inc('penetrated', requested)
        mycelium.memory.log_phase('penetrate', 0, 'requested=' + str(requested))

    return requested