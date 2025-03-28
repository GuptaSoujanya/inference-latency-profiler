import time
from dataclasses import dataclass, field
from typing import List
from .timer import calculate_percentiles

@dataclass
class RequestLatencyRecord:
    prompt_tokens: int
    completion_tokens: int
    ttft_ms: float
    inter_token_latencies_ms: List[float] = field(default_factory=list)
    total_time_ms: float = 0.0

    @property
    def mean_itl_ms(self) -> float:
        if not self.inter_token_latencies_ms:
            return 0.0
        return sum(self.inter_token_latencies_ms) / len(self.inter_token_latencies_ms)

    @property
    def throughput_tokens_per_sec(self) -> float:
        if self.total_time_ms <= 0:
            return 0.0
        return (self.completion_tokens / (self.total_time_ms / 1000.0))

@dataclass
class AggregatedProfileStats:
    total_requests: int
    total_tokens_generated: int
    mean_ttft_ms: float
    ttft_percentiles: dict
    mean_itl_ms: float
    itl_percentiles: dict
    mean_throughput: float
