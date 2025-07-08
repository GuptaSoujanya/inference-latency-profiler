import unittest
from profiler.collector import RequestLatencyRecord

class TestCollector(unittest.TestCase):
    def test_record_throughput(self):
        rec = RequestLatencyRecord(
            prompt_tokens=32,
            completion_tokens=50,
            ttft_ms=50.0,
            inter_token_latencies_ms=[10.0] * 49,
            total_time_ms=1000.0 # 1 second
        )
        self.assertEqual(rec.throughput_tokens_per_sec, 50.0)
        self.assertEqual(rec.mean_itl_ms, 10.0)

if __name__ == "__main__":
    unittest.main()
