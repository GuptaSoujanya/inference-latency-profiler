import unittest
from profiler.config import ProfilerConfig
from profiler.engine import LatencyProfiler

class TestProfilerEngine(unittest.TestCase):
    def test_run_benchmark(self):
        cfg = ProfilerConfig(num_requests=3, generate_tokens=8)
        profiler = LatencyProfiler(cfg)
        stats, records = profiler.run_benchmark()
        self.assertEqual(len(records), 3)
        self.assertGreater(stats.mean_ttft_ms, 0.0)
        self.assertGreater(stats.mean_itl_ms, 0.0)
        self.assertGreater(stats.mean_throughput, 0.0)

if __name__ == "__main__":
    unittest.main()
