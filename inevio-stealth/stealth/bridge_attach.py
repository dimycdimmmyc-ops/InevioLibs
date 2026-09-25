"""Stealth: bridge integration with spore-net."""
import base64
import time

from .engine import PolymorphicEncoder


class StealthReceiver:
    """Storage for received stealth payloads."""
    def __init__(self):
        self.messages = []

    def add(self, from_who, seq, text):
        self.messages.append({
            'from': from_who,
            'seq': seq,
            'text': text,
            'received_at': time.time(),
        })

    def get_all(self):
        return list(self.messages)

    def clear(self):
        self.messages.clear()


RECEIVER = StealthReceiver()


def attach_bridge(bridge, receiver=None):
    """Subscribe to incoming stealth payloads."""
    if receiver is None:
        receiver = RECEIVER

    def _on_payload(payload, from_who):
        try:
            body = base64.b64decode(payload.get('body', ''))
            text = PolymorphicEncoder.decode({'body': body}).decode('utf-8', 'replace')
            receiver.add(from_who, payload.get('seq'), text)
        except Exception as e:
            print('[stealth-bridge] decode error: ' + str(e))

    bridge.subscribe('stealth.payload', _on_payload)
    return receiver


def send_via_spore(bridge, payload, target):
    """Send payload through spore-net with polymorphic masking."""
    if isinstance(payload, str):
        payload = payload.encode('utf-8')

    frag = PolymorphicEncoder().encode(payload, 'SPORE')

    ok = bridge.send(target, 'stealth.payload', {
        'seq': frag['seq'],
        'body': base64.b64encode(frag['body']).decode(),
        'delay_ms': frag['delay_ms'],
    })

    return {
        'success': ok,
        'seq': frag['seq'],
        'size': len(frag['body']),
        'target': target,
    }