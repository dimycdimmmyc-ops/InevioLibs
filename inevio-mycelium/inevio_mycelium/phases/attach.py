"""ATTACH — закрепление на найденных узлах."""
import time
from ..constants import TOPIC_HELLO


def attach(mycelium, node):
    """Закрепиться на узле."""
    addr = node.get('addr', '')
    if not addr:
        return False

    # Если уже закреплены — выходим
    if addr in mycelium.memory.attached:
        return True

    # Отправляем hello
    ok = mycelium.env.send(addr, TOPIC_HELLO, {
        'from': mycelium.env.name,
        'depth': node.get('depth', 1),
        'ts': time.time(),
    })

    if ok:
        if mycelium.memory.attach(addr, node):
            mycelium.stats.inc('attached')
            mycelium.env.log('info', '[Mycelium/attach] ' + addr)
            return True
    return False


def attach_all(mycelium, nodes):
    """Закрепиться на всех найденных."""
    attached = 0
    for node in nodes:
        if attach(mycelium, node):
            attached += 1
    return attached