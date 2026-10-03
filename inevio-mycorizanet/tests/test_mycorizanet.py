"""Tests for inevio-mycorizanet."""
import time
import unittest

from inevio_mycorizanet import (
    MycorrhizaOverlay, Membrane, TrailTable, SymbiosisLedger,
    QuorumSensor, OsmoticBalancer, ImmuneMemory, SporeAddressing,
    name_for, ula_for, TransportSelector, UDPTransport,
)


class TestAddressing(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(name_for("node_a"), name_for("node_a"))
        self.assertTrue(ula_for("node_a").startswith("fd"))

    def test_register_resolve(self):
        z = SporeAddressing()
        rec = z.register("node_a")
        got = z.resolve(rec["name"])
        self.assertIsNotNone(got)
        self.assertEqual(got["address"], rec["address"])
        self.assertEqual(got["node_id"], "node_a")
        self.assertEqual(z.reverse(rec["address"])["node_id"], "node_a")


class TestMembrane(unittest.TestCase):
    def test_seal_verify(self):
        m = Membrane(b"secret", "A")
        blob = m.seal(b"hello", "B")
        self.assertTrue(m.verify(blob, "B"))
        self.assertFalse(m.verify(blob, "C"))
        self.assertEqual(m.payload(blob), b"hello")


class TestTrails(unittest.TestCase):
    def test_deposit_penalize(self):
        t = TrailTable()
        t.deposit("d", "h1", rtt=0.1)
        t.deposit("d", "h1", rtt=0.1)
        t.deposit("d", "h2", rtt=0.9)
        self.assertEqual(t.next_hop("d"), "h1")
        t.penalize("d", "h1", 0.0)
        self.assertEqual(t.next_hop("d"), "h2")

    def test_evaporate(self):
        t = TrailTable()
        t.deposit("d", "h1")
        t.evaporate(3600)
        self.assertIsNone(t.next_hop("d"))


class TestSymbiosis(unittest.TestCase):
    def test_mutual(self):
        s = SymbiosisLedger()
        s.record_given("p", 5)
        self.assertFalse(s.mutual("p"))
        s.record_received("p", 5)
        self.assertTrue(s.mutual("p"))
        self.assertEqual(s.fairness("p"), 1.0)


class TestQuorum(unittest.TestCase):
    def test_fires(self):
        fired = []
        q = QuorumSensor()
        q.on_quorum.append(lambda t, c: fired.append(t))
        q.signal("x")
        q.signal("x")
        self.assertEqual(len(fired), 0)
        q.signal("x")
        self.assertEqual(fired, ["x"])


class TestOsmosis(unittest.TestCase):
    def test_downhill(self):
        o = OsmoticBalancer()
        o.set_load(80)
        o.report_neighbor("n1", 20)
        o.report_neighbor("n2", 60)
        self.assertEqual(o.downhill(), "n1")
        self.assertEqual(o.gradient("n1"), 60)


class TestImmune(unittest.TestCase):
    def test_learning(self):
        im = ImmuneMemory()
        im.learn_self("s")
        self.assertFalse(im.blocked("s"))
        im.attack("e")
        im.attack("e")
        self.assertFalse(im.blocked("e"))
        im.attack("e")
        self.assertTrue(im.blocked("e"))
        im.tolerate("e", ttl=10)
        self.assertFalse(im.blocked("e"))


class TestTransportSelector(unittest.TestCase):
    def test_choose_udp(self):
        udp = UDPTransport(port=0)
        sel = TransportSelector([udp])
        t = sel.choose()
        self.assertIsNotNone(t)
        self.assertEqual(t.name, "udp")


class TestOverlay(unittest.TestCase):
    def test_send_receive(self):
        a = MycorrhizaOverlay("A", b"s", transports=[UDPTransport(port=0)])
        b = MycorrhizaOverlay("B", b"s", transports=[UDPTransport(port=0)])
        a.add_peer("B")
        blob = a.membrane.seal(b"ping", "B")
        r = b.receive("A", blob)
        self.assertEqual(r["status"], "own")
        self.assertEqual(r["payload"], b"ping")

    def test_foreign(self):
        a = MycorrhizaOverlay("A", b"s", transports=[UDPTransport(port=0)])
        b = MycorrhizaOverlay("B", b"s", transports=[UDPTransport(port=0)])
        a.add_peer("B")
        blob = a.membrane.seal(b"ping", "B")
        r = b.receive("C", blob)
        self.assertEqual(r["status"], "foreign")


if __name__ == '__main__':
    unittest.main()