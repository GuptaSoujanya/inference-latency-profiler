import time
import random
from typing import Iterator
from .base import BaseBackend

class MockStreamingBackend(BaseBackend):
    """
    Simulates realistic server-side LLM inference latency.
    Simulates:
    - Time-to-First-Token (TTFT): Pre-fill phase (prompt processing, KV cache allocation) ~ 45-90ms
    - Inter-Token-Latency (ITL): Decode phase autoregressive steps ~ 12-25ms per token
    """

    def __init__(self, base_ttft_ms: float = 65.0, base_itl_ms: float = 18.0, jitter: float = 0.2):
        self.base_ttft_ms = base_ttft_ms
        self.base_itl_ms = base_itl_ms
        self.jitter = jitter

    def stream_generate(self, prompt: str, max_tokens: int = 64) -> Iterator[str]:
        # Simulate pre-fill delay (TTFT)
        prefill_delay = (self.base_ttft_ms * (1.0 + random.uniform(-self.jitter, self.jitter))) / 1000.0
        time.sleep(max(0.005, prefill_delay))
        yield "The"

        # Simulate decode tokens
        sample_words = [" model", " generated", " high", " throughput", " tokens", " efficiently", " under", " load", "."]
        for i in range(max_tokens - 1):
            decode_delay = (self.base_itl_ms * (1.0 + random.uniform(-self.jitter, self.jitter))) / 1000.0
            time.sleep(max(0.002, decode_delay))
            word = sample_words[i % len(sample_words)]
            yield word
