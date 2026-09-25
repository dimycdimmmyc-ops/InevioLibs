"""Test Stealth integration with SporeBridge."""
import time
import unittest

from spore_bridge import SporeBridge
from spore.soil import ПочваSocket
from stealth import attach_bridge, send_via_spore


class TestStealthBridge(unittest.TestCase):

    def test_payload_propagation(self):
        A = SporeBridge('st-A', soils=[ПочваSocket('0.0.0.0', 12200)])
        B = SporeBridge('st-B', soils=[ПочваSocket('0.0.0.0', 12201)])

        receiver_b = attach_bridge(B)

        B.loop(blocking=False)
        time.sleep(0.5)

        result = send_via_spore(A, 'secret message', ('127.0.0.1', 12201))
        self.assertTrue(result['success'], 'Send failed')

        time.sleep(1.5)

        messages = receiver_b.get_all()
        self.assertGreater(len(messages), 0, 'B did not receive payload')
        self.assertEqual(messages[0]['text'], 'secret message',
                         'Payload was corrupted')

        A.hibernate()
        B.hibernate()


if __name__ == '__main__':
    unittest.main()