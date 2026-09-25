"""Tests for inevio-mycelium."""
import time
import unittest

from inevio_mycelium import Mycelium, EnvMock


class TestMycelium(unittest.TestCase):

    def test_create(self):
        env = EnvMock('test-node')
        my = Mycelium(env, max_depth=5)
        self.assertEqual(my.max_depth, 5)
        self.assertIsNotNone(my.memory)
        self.assertIsNotNone(my.stats)

    def test_scout(self):
        env = EnvMock('test-node')
        env.add_discover('10.0.0.2')
        env.add_discover('10.0.0.3')
        my = Mycelium(env, max_depth=5)
        from inevio_mycelium.phases import scout
        found = scout(my)
        self.assertGreater(len(found), 0)
        self.assertGreaterEqual(my.stats.get('found'), 2)

    def test_attach(self):
        env = EnvMock('test-node')
        my = Mycelium(env, max_depth=5)
        from inevio_mycelium.phases.attach import attach
        ok = attach(my, {'addr': '10.0.0.2', 'type': 'lan_device', 'depth': 1})
        self.assertTrue(ok)
        self.assertIn('10.0.0.2', my.memory.attached)

    def test_penetrate(self):
        env = EnvMock('test-node')
        my = Mycelium(env, max_depth=5)
        from inevio_mycelium.phases.attach import attach
        from inevio_mycelium.phases import penetrate
        attach(my, {'addr': '10.0.0.2', 'type': 'lan_device', 'depth': 1})
        requested = penetrate(my)
        self.assertGreaterEqual(requested, 1)

    def test_merge(self):
        env = EnvMock('test-node')
        my = Mycelium(env, max_depth=5)
        from inevio_mycelium.phases import merge
        other_map = {
            'from': 'other-node',
            'nodes': [
                {'addr': '10.0.0.5', 'type': 'lan_device', 'depth': 2},
                {'addr': '10.0.0.6', 'type': 'router', 'depth': 3},
            ],
        }
        added = merge(my, other_map)
        self.assertEqual(added, 2)
        self.assertIn('10.0.0.5', my.memory.nodes)
        self.assertIn('10.0.0.6', my.memory.nodes)

    def test_hello_handler(self):
        env = EnvMock('test-node')
        my = Mycelium(env, max_depth=5)
        # Симулируем hello
        my._on_hello({'from': '10.0.0.7', 'depth': 2}, '10.0.0.7')
        self.assertIn('10.0.0.7', my.memory.nodes)

    def test_stats(self):
        env = EnvMock('test-node')
        my = Mycelium(env, max_depth=5)
        st = my.get_stats()
        self.assertIn('cycles', st)
        self.assertIn('nodes_in_memory', st)
        self.assertIn('depth_max', st)


if __name__ == '__main__':
    unittest.main()