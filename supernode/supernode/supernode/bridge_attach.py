"""Supernode: bridge integration with spore-net."""
from .manager import SuperNodeManager


def attach_bridge(manager, bridge):
    """Attach SporeBridge to SuperNodeManager."""
    manager._bridge = bridge
    bridge.subscribe('supernode.experience', manager._on_bridge_experience)
    return manager


def _on_bridge_experience(self, payload, from_who):
    """Callback: experience packet received from another super-node."""
    self.apply_experience(payload)


def broadcast_via_spore(self, node_id, interval=60.0):
    """Broadcast experience via spore-net using bridge.broadcast()."""
    bridge = getattr(self, '_bridge', None)
    if bridge is None:
        return 0

    packet = self.broadcast_payload(node_id, interval)
    if packet is None:
        return 0

    return bridge.broadcast('supernode.experience', packet)


SuperNodeManager._on_bridge_experience = _on_bridge_experience
SuperNodeManager.broadcast_via_spore = broadcast_via_spore