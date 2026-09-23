import unittest
from sporerecon.recon import classify, neighbors_estimate, full_recon

class TestRecon(unittest.TestCase):
    def test_classify(self):
        self.assertEqual(classify("MTS Router 5G", [], 5), "cellular-router")
        self.assertEqual(classify("cafe free wifi", [], 5), "public-hotspot")
        self.assertEqual(classify("HomeNet", ["8.8.8.8"], 5), "consumer-router")
        self.assertEqual(classify("x", [], 1), "direct-isp")
        self.assertEqual(classify("x", [], 9), "deep-infra")
    def test_neighbors_int(self):
        self.assertIsInstance(neighbors_estimate(timeout=2), int)
    def test_full_recon_keys(self):
        r = full_recon("TestSSID", "aa:bb:cc:dd:ee:ff", timeout=2)
        for k in ("ssid", "bssid", "dns_servers", "depth", "isp",
                  "neighbors_estimate", "infra_type", "recon_at"):
            self.assertIn(k, r)

if __name__ == "__main__":
    unittest.main()
