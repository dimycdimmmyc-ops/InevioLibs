"""Tests for SporeBridge."""
import unittest
import time

from spore_bridge import SporeBridge
from spore.soil import ПочваSocket


class TestBridge(unittest.TestCase):

    def test_create(self):
        bridge = SporeBridge('test-1', soils=[ПочваSocket('0.0.0.0', 8710)])
        self.assertIsNotNone(bridge.node)
        self.assertEqual(bridge.name, 'test-1')
        bridge.hibernate()

    def test_status(self):
        bridge = SporeBridge('test-2', soils=[ПочваSocket('0.0.0.0', 8711)])
        st = bridge.status()
        self.assertIn('имя', st)
        self.assertEqual(st['имя'], 'test-2')
        self.assertIn('почва', st)
        bridge.hibernate()

    def test_exchange(self):
        """Two bridges exchange messages."""
        A = SporeBridge('A', soils=[ПочваSocket('0.0.0.0', 8712)])
        B = SporeBridge('B', soils=[ПочваSocket('0.0.0.0', 8713)])

        received = []

        def handler(payload, from_who):
            received.append((payload, from_who))

        B.subscribe('echo', handler)
        B.loop(blocking=False)

        time.sleep(0.5)

        A.send(('127.0.0.1', 8713), 'echo', {'msg': 'hello'})
        time.sleep(1.5)

        self.assertTrue(len(received) > 0, 'Message not delivered')

        A.hibernate()
        B.hibernate()


if __name__ == '__main__':
    unittest.main()