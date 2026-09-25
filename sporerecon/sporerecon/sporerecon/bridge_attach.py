"""Sporerecon: bridge integration with spore-net."""
from .recon import full_recon


class ReconStorage:
    def __init__(self):
        self.data = {}

    def add(self, from_who, payload):
        self.data[from_who] = payload

    def get(self, from_who=None):
        if from_who is None:
            return dict(self.data)
        return self.data.get(from_who)


STORAGE = ReconStorage()


def attach_bridge(bridge, storage=None):
    if storage is None:
        storage = STORAGE.data

    def _on_findings(payload, from_who):
        storage[from_who] = payload

    bridge.subscribe('sporerecon.findings', _on_findings)
    return storage


def broadcast_recon(bridge, ssid='', bssid=''):
    """Run local recon and broadcast findings via bridge.broadcast()."""
    findings = full_recon(ssid, bssid)
    sent = bridge.broadcast('sporerecon.findings', findings)
    return {'findings': findings, 'sent_to': sent}