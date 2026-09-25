"""MERGE — слияние карт от других грибниц."""


def merge(mycelium, other_map):
    """Слить чужую карту со своей."""
    added = 0
    sender = other_map.get('from', '?')

    for node in other_map.get('nodes', []):
        addr = node.get('addr', '')
        if not addr or addr in mycelium.memory.nodes:
            continue

        new_node = {
            'addr': addr,
            'type': node.get('type', 'unknown'),
            'depth': node.get('depth', 1) + 1,
            'source': 'merge:' + sender,
        }
        if mycelium.memory.add_node(addr, new_node):
            added += 1

    if added > 0:
        mycelium.stats.inc('maps_merged')
        mycelium.stats.inc('nodes_from_merge', added)
        mycelium.memory.log_phase('merge', 0, 'from=' + sender + ' added=' + str(added))

    return added