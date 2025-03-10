from dataclasses import dataclass
from typing import Optional

@dataclass
class ProfilerConfig:
    backend: str = "mock"
    model_name: str = "qwen-2.5-7b"
    endpoint_url: Optional[str] = None
    num_requests: int = 10
    concurrency: int = 1
    prompt_tokens: int = 128
    generate_tokens: int = 64
