import unittest
from profiler.timer import calculate_percentiles
from profiler.engine import LatencyProfiler

class TestProfiler(unittest.TestCase):
    def test_percentiles(self):
        vals = list(range(1, 101))
        p = calculate_percentiles(vals)
        self.assertEqual(p["p50"], 50)
        self.assertEqual(p["p99"], 99)

    def test_profiler_engine(self):
        p = LatencyProfiler(base_ttft_ms=5.0, base_itl_ms=2.0)
        res = p.profile_run(num_tokens=5)
        self.assertGreater(res["throughput_tok_s"], 0)

if __name__ == "__main__":
    unittest.main()
