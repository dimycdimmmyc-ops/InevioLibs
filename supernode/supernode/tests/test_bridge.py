"""Test SuperNode integration with SporeBridge."""
import time
import unittest

from spore_bridge import SporeBridge
from spore.soil import ПочваSocket
from supernode import SuperNodeManager, attach_bridge


class TestSupernodeBridge(unittest.TestCase):

    def test_experience_propagation(self):
        A = SporeBridge('sn-A', soils=[ПочваSocket('0.0.0.0', 12000)])
        B = SporeBridge('sn-B', soils=[ПочваSocket('0.0.0.0', 12001)])

        m_a = SuperNodeManager()
        m_b = SuperNodeManager()
        attach_bridge(m_a, A)
        attach_bridge(m_b, B)

        B.loop(blocking=False)
        time.sleep(0.5)

        # Знакомство: A узнаёт о B
        A.send(('127.0.0.1', 12001), 'hello', {'msg': 'hi'})
        time.sleep(0.3)

        node = {
            'node_id': 'n1',
            'name': 'node-1',
            'type': 'worker',
            'seen_count': 100,
        }
        evo = {'best_fitness': 0.95, 'best_genome': 'abc'}
        dl = {'node-1': {'tried': ['a', 'b', 'c', 'd', 'e'],
                         'succeeded': ['a', 'b', 'c', 'd', 'e']}}

        promoted = m_a.promote(node, evo, dl)
        self.assertTrue(promoted)

        # Теперь broadcast найдёт B
        sent = m_a.broadcast_via_spore('n1', interval=0)
        self.assertGreater(sent, 0, 'No broadcast happened')

        time.sleep(1.5)

        stats_b = m_b.get_stats()
        self.assertGreater(stats_b['applied_experience'], 0,
                           'B did not receive experience')

        A.hibernate()
        B.hibernate()


if __name__ == '__main__':
    unittest.main()