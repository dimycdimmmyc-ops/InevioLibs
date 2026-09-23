import threading, unittest
from stealth.engine import (BayesianUpdater, PolymorphicEncoder,
                            StealthEngine, StealthListener)

class TestBayes(unittest.TestCase):
    def test_update(self):
        b = BayesianUpdater()
        for _ in range(5): b.update("HTTP-POST", True)
        b.update("HTTP-POST", False)
        self.assertGreater(b.p("HTTP-POST"), 0.7)
        self.assertEqual(b.p("DNS"), 0.5)

class TestEncoder(unittest.TestCase):
    def test_roundtrip(self):
        f = PolymorphicEncoder().encode(b"hi", "HTTP-POST")
        self.assertGreaterEqual(len(f["body"]), 350)
        self.assertEqual(PolymorphicEncoder.decode(f), b"hi")

class TestLoopback(unittest.TestCase):
    def test_send_receive(self):
        lis = StealthListener(port=0)
        t = threading.Thread(target=lis.serve_forever, daemon=True); t.start()
        try:
            res = StealthEngine().send("hello stealth", "127.0.0.1:%d" % lis.port)
            self.assertTrue(res["success"])
            self.assertTrue(any(m["text"] == "hello stealth"
                                for m in lis.messages()))
        finally:
            lis.shutdown()
    def test_send_fail(self):
        self.assertFalse(StealthEngine().send("x", "127.0.0.1:9")["success"])

if __name__ == "__main__":
    unittest.main()
