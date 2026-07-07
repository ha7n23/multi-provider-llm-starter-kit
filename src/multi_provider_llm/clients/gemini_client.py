from collections.abc import Iterator

from google import genai
from google.genai import types

from multi_provider_llm.config import settings
from multi_provider_llm.exceptions import LLMProviderError, MissingAPIKeyError


class GeminiClient:
    """Gemini LLM client using the Google GenAI SDK."""

    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise MissingAPIKeyError("GEMINI_API_KEY is missing.")

        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model

    def generate(self, prompt: str) -> str:
        """Generate a complete Gemini response."""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="You are a concise and practical AI assistant.",
                    max_output_tokens=settings.max_output_tokens,
                    temperature=settings.temperature,
                ),
            )

            return response.text or ""

        except Exception as error:
            raise LLMProviderError(f"Gemini API call failed: {error}") from error

    def generate_stream(self, prompt: str) -> Iterator[str]:
        """Generate a streaming Gemini response."""
        try:
            stream = self.client.models.generate_content_stream(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="You are a concise and practical AI assistant.",
                    max_output_tokens=settings.max_output_tokens,
                    temperature=settings.temperature,
                ),
            )

            for chunk in stream:
                if chunk.text:
                    yield chunk.text

        except Exception as error:
            raise LLMProviderError(f"Gemini streaming API call failed: {error}") from error