from collections.abc import Iterator

from groq import Groq

from multi_provider_llm.config import settings
from multi_provider_llm.exceptions import LLMProviderError, MissingAPIKeyError


class GroqClient:
    """Groq LLM client using Groq's chat completions API."""

    def __init__(self) -> None:
        if not settings.groq_api_key:
            raise MissingAPIKeyError("GROQ_API_KEY is missing.")

        self.client = Groq(api_key=settings.groq_api_key)
        self.model = settings.groq_model

    def generate(self, prompt: str) -> str:
        """Generate a complete Groq response."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a concise and practical AI assistant.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                max_tokens=settings.max_output_tokens,
                temperature=settings.temperature,
            )

            return response.choices[0].message.content or ""

        except Exception as error:
            raise LLMProviderError(f"Groq API call failed: {error}") from error

    def generate_stream(self, prompt: str) -> Iterator[str]:
        """Generate a streaming Groq response."""
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a concise and practical AI assistant.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                max_tokens=settings.max_output_tokens,
                temperature=settings.temperature,
                stream=True,
            )

            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta

        except Exception as error:
            raise LLMProviderError(f"Groq streaming API call failed: {error}") from error