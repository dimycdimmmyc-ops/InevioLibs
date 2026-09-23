import unittest
from supernode.manager import SuperNodeManager
NODE = {"node_id": "n1", "name": "RT-1", "type": "wifi", "seen_count": 20}
EVO = {"best_fitness": 1.0}
DEL = {"RT-1": {"tried": [1]*10, "succeeded": [1]*10, "last_method": "HTTPS-POST"}}

class TestSuper(unittest.TestCase):
    def test_promote_ok(self):
        m = SuperNodeManager()
        self.assertTrue(m.promote(NODE, EVO, DEL))
        self.assertTrue(m.is_super("n1"))
        self.assertEqual(m.get_stats()["count"], 1)
    def test_promote_low_fitness(self):
        self.assertFalse(SuperNodeManager().promote(NODE, {"best_fitness": 0.5}, DEL))
    def test_broadcast_interval(self):
        m = SuperNodeManager(); m.promote(NODE, EVO, DEL)
        self.assertIsNotNone(m.broadcast_payload("n1", 60))
        self.assertIsNone(m.broadcast_payload("n1", 60))
    def test_apply_experience(self):
        m = SuperNodeManager()
        self.assertEqual(m.apply_experience({"from": "x"})["from"], "x")
    def test_persistence(self):
        import tempfile, os
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "s.json")
            SuperNodeManager(state_file=f).promote(NODE, EVO, DEL)
            self.assertTrue(SuperNodeManager(state_file=f).is_super("n1"))

if __name__ == "__main__":
    unittest.main()
