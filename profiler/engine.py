import time
import random
from .timer import calculate_percentiles

class LatencyProfiler:
    def __init__(self, base_ttft_ms=55.0, base_itl_ms=18.0):
        self.base_ttft_ms = base_ttft_ms
        self.base_itl_ms = base_itl_ms

    def profile_run(self, num_tokens=32):
        start = time.perf_counter()
        time.sleep(self.base_ttft_ms / 1000.0)
        ttft = (time.perf_counter() - start) * 1000.0

        itl_deltas = []
        for _ in range(num_tokens - 1):
            t0 = time.perf_counter()
            time.sleep((self.base_itl_ms * random.uniform(0.9, 1.1)) / 1000.0)
            itl_deltas.append((time.perf_counter() - t0) * 1000.0)

        total_time_s = (ttft + sum(itl_deltas)) / 1000.0
        throughput = num_tokens / total_time_s if total_time_s > 0 else 0.0

        return {
            "tokens": num_tokens,
            "ttft_ms": round(ttft, 2),
            "itl_mean_ms": round(sum(itl_deltas)/len(itl_deltas), 2),
            "itl_p50": calculate_percentiles(itl_deltas)["p50"],
            "itl_p99": calculate_percentiles(itl_deltas)["p99"],
            "throughput_tok_s": round(throughput, 2)
        }

    def export_summary_json(self): return {}
