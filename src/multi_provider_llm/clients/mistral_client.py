from collections.abc import Iterator

from mistralai.client import Mistral

from multi_provider_llm.config import settings
from multi_provider_llm.exceptions import LLMProviderError, MissingAPIKeyError


class MistralClient:
    """Mistral LLM client using Mistral's chat completions API."""

    def __init__(self) -> None:
        if not settings.mistral_api_key:
            raise MissingAPIKeyError("MISTRAL_API_KEY is missing.")

        self.client = Mistral(api_key=settings.mistral_api_key)
        self.model = settings.mistral_model

    def generate(self, prompt: str) -> str:
        """Generate a complete Mistral response."""
        try:
            response = self.client.chat.complete(
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

            message = response.choices[0].message
            if message is None:
                return ""

            content = message.content
            if isinstance(content, str):
                return content

            return ""

        except Exception as error:
            raise LLMProviderError(f"Mistral API call failed: {error}") from error

    def generate_stream(self, prompt: str) -> Iterator[str]:
        """Generate a streaming Mistral response."""
        try:
            stream = self.client.chat.stream(
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

            for event in stream:
                delta = event.data.choices[0].delta
                if delta is None:
                    continue

                content = delta.content
                if isinstance(content, str):
                    yield content
                elif content is not None:
                    yield str(content)

        except Exception as error:
            raise LLMProviderError(f"Mistral streaming API call failed: {error}") from error