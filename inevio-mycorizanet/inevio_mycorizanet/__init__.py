"""МИКОРИЗАnet — живой overlay-организм."""
__version__ = '1.0.0'

import os

from .addressing import SporeAddressing, name_for, ula_for
from .membrane import Membrane
from .trails import TrailTable
from .symbiosis import SymbiosisLedger
from .quorum import QuorumSensor
from .osmosis import OsmoticBalancer
from .immune import ImmuneMemory
from .overlay import MycorrhizaOverlay
from .transport import (
    Transport, TransportSelector,
    UDPTransport, TCPTransport, DNSTransport,
    ICMPTransport, HTTPTransport,
)

__all__ = [
    '__version__',
    'SporeAddressing', 'name_for', 'ula_for',
    'Membrane',
    'TrailTable',
    'SymbiosisLedger',
    'QuorumSensor',
    'OsmoticBalancer',
    'ImmuneMemory',
    'MycorrhizaOverlay',
    'Transport', 'TransportSelector',
    'UDPTransport', 'TCPTransport', 'DNSTransport',
    'ICMPTransport', 'HTTPTransport',
    'create_overlay',
]


def create_overlay(self_id, secret=b"inevio_forever", data_dir=None,
                   transports=None, resolver_port=None):
    """Точка входа: живой overlay-организм."""
    dd = data_dir or os.path.join(os.getcwd(), "data")
    os.makedirs(dd, exist_ok=True)

    if transports is None:
        transports = [UDPTransport(), TCPTransport(), DNSTransport(),
                      ICMPTransport(), HTTPTransport()]

    ov = MycorrhizaOverlay(self_id, secret,
                            zone_file=os.path.join(dd, "spore_zone.json"),
                            transports=transports)
    ov.start()
    if resolver_port:
        ov.start_resolver(port=resolver_port)
    return ov