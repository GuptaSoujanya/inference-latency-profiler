import unittest
from profiler.timer import calculate_percentiles

class TestTimerPercentiles(unittest.TestCase):
    def test_percentile_calculation(self):
        values = list(range(1, 101)) # 1 to 100
        p = calculate_percentiles(values)
        self.assertAlmostEqual(p["p50"], 50.5, places=1)
        self.assertAlmostEqual(p["p90"], 90.1, places=1)
        self.assertAlmostEqual(p["p99"], 99.01, places=1)

    def test_empty_values(self):
        p = calculate_percentiles([])
        self.assertEqual(p["p50"], 0.0)

if __name__ == "__main__":
    unittest.main()
