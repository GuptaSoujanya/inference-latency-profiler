from abc import ABC, abstractmethod
from typing import Iterator

class BaseBackend(ABC):
    """Abstract interface for streaming token generator backends."""

    @abstractmethod
    def stream_generate(self, prompt: str, max_tokens: int = 64) -> Iterator[str]:
        """Yield token chunks as they arrive from the inference engine."""
        pass
