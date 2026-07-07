from collections.abc import Iterator
from typing import Protocol

class LLMClient(Protocol):
    """Common interface that all LLM clients must follow."""

    def generate(self, prompt: str) -> str:
        """Generate a complete response from a prompt"""
        ...

    def generate_stream(self, prompt: str) -> Iterator[str]:
        """Generate a response chunk by chunk"""
        ...


        