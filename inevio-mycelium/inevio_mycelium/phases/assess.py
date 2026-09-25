"""ASSESS — оценка узла: куда идти глубже."""


def assess(mycelium, node):
    """Оценить узел."""
    addr = node.get('addr', '')
    if not addr:
        return {'action': 'skip', 'reason': 'no_addr'}

    # Уже закреплены — пропускаем
    if addr in mycelium.memory.attached:
        return {'action': 'skip', 'reason': 'already_attached'}

    # Слишком глубоко
    depth = node.get('depth', 1)
    if depth >= mycelium.max_depth:
        return {'action': 'skip', 'reason': 'too_deep'}

    # Тип узла
    node_type = node.get('type', 'unknown')

    if node_type in ('router', 'gateway'):
        return {'action': 'penetrate', 'reason': 'gateway', 'priority': 0.9}
    if node_type == 'inevionet':
        return {'action': 'attach', 'reason': 'inevionet', 'priority': 0.8}
    if node_type == 'lan_device':
        return {'action': 'attach', 'reason': 'lan', 'priority': 0.6}
    if node_type == 'spore_resonance':
        return {'action': 'attach', 'reason': 'spore', 'priority': 0.7}

    return {'action': 'attach', 'reason': 'fallback', 'priority': 0.3}