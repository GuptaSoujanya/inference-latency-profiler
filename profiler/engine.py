import time
from typing import List
from .config import ProfilerConfig
from .backends.base import BaseBackend
from .backends.mock_backend import MockStreamingBackend
from .collector import RequestLatencyRecord, AggregatedProfileStats
from .timer import calculate_percentiles
from .telemetry.memory import get_system_memory_snapshot

class LatencyProfiler:
    """Profiles TTFT and ITL across streaming requests."""

    def __init__(self, config: ProfilerConfig, backend: BaseBackend = None):
        self.config = config
        self.backend = backend or MockStreamingBackend()

    def profile_single_request(self, prompt: str = "Benchmark test prompt") -> RequestLatencyRecord:
        start_time = time.perf_counter()
        token_times = []
        token_count = 0

        stream = self.backend.stream_generate(prompt, max_tokens=self.config.generate_tokens)
        first_token_time = None

        for chunk in stream:
            now = time.perf_counter()
            token_count += 1
            if first_token_time is None:
                first_token_time = now
            token_times.append(now)

        end_time = time.perf_counter()

        ttft_ms = (first_token_time - start_time) * 1000.0 if first_token_time else 0.0
        itl_ms_list = []
        for i in range(1, len(token_times)):
            delta_ms = (token_times[i] - token_times[i-1]) * 1000.0
            itl_ms_list.append(delta_ms)

        total_ms = (end_time - start_time) * 1000.0
        return RequestLatencyRecord(
            prompt_tokens=self.config.prompt_tokens,
            completion_tokens=token_count,
            ttft_ms=round(ttft_ms, 2),
            inter_token_latencies_ms=itl_ms_list,
            total_time_ms=round(total_ms, 2)
        )

    def run_benchmark(self) -> (AggregatedProfileStats, List[RequestLatencyRecord]):
        records = []
        for _ in range(self.config.num_requests):
            records.append(self.profile_single_request())

        all_ttft = [r.ttft_ms for r in records]
        all_itl = []
        for r in records:
            all_itl.extend(r.inter_token_latencies_ms)

        all_throughputs = [r.throughput_tokens_per_sec for r in records]
        total_tokens = sum(r.completion_tokens for r in records)

        stats = AggregatedProfileStats(
            total_requests=len(records),
            total_tokens_generated=total_tokens,
            mean_ttft_ms=round(sum(all_ttft) / len(all_ttft), 2) if all_ttft else 0.0,
            ttft_percentiles=calculate_percentiles(all_ttft),
            mean_itl_ms=round(sum(all_itl) / len(all_itl), 2) if all_itl else 0.0,
            itl_percentiles=calculate_percentiles(all_itl),
            mean_throughput=round(sum(all_throughputs) / len(all_throughputs), 2) if all_throughputs else 0.0
        )
        return stats, records
