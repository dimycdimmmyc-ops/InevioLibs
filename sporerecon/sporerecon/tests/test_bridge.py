"""Test SporeRecon integration with SporeBridge."""
import time
import unittest

from spore_bridge import SporeBridge
from spore.soil import ПочваSocket
from sporerecon import attach_bridge, broadcast_recon


class TestSporereconBridge(unittest.TestCase):

    def test_findings_propagation(self):
        A = SporeBridge('rec-A', soils=[ПочваSocket('0.0.0.0', 12100)])
        B = SporeBridge('rec-B', soils=[ПочваSocket('0.0.0.0', 12101)])

        storage_b = {}
        attach_bridge(B, storage_b)

        B.loop(blocking=False)
        time.sleep(0.5)

        # Знакомство
        A.send(('127.0.0.1', 12101), 'hello', {'msg': 'hi'})
        time.sleep(0.3)

        # A делает recon и рассылает
        result = broadcast_recon(A, ssid='TestNet', bssid='aa:bb:cc:dd:ee:ff')
        self.assertGreater(result['sent_to'], 0, 'Recon was not sent')

        time.sleep(2.0)

        # B получил
        self.assertGreater(len(storage_b), 0, 'B did not receive findings')

        A.hibernate()
        B.hibernate()


if __name__ == '__main__':
    unittest.main()