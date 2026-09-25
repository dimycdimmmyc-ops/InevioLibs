"""SCOUT — поиск новых соседей."""
from ..constants import BATCH_SCOUT


def scout(mycelium):
    """Найти новых соседей."""
    env = mycelium.env
    found = []

    # 1. Уже известные
    for addr in env.neighbors():
        if addr not in mycelium.memory.nodes:
            found.append({
                'addr': addr, 'source': 'existing',
                'depth': 1, 'type': 'unknown',
            })

    # 2. Discovery через споры
    for addr in env.discover():
        if addr not in mycelium.memory.nodes:
            found.append({
                'addr': addr, 'source': 'spore',
                'depth': 1, 'type': 'spore_resonance',
            })

    # Регистрируем в памяти
    new_count = 0
    for node in found[:BATCH_SCOUT]:
        if mycelium.memory.add_node(node['addr'], node):
            new_count += 1

    mycelium.stats.inc('scouts')
    mycelium.stats.inc('found', len(found))
    mycelium.memory.log_phase('scout', 0, 'found=' + str(len(found)))

    if new_count > 0:
        env.log('info', '[Mycelium/scout] new=' + str(new_count))

    return found