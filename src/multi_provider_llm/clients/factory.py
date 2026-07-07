from multi_provider_llm.clients.base import LLMClient
from multi_provider_llm.clients.gemini_client import GeminiClient
from multi_provider_llm.clients.groq_client import GroqClient
from multi_provider_llm.clients.mistral_client import MistralClient
from multi_provider_llm.clients.mock_client import MockLLMClient
from multi_provider_llm.config import settings
from multi_provider_llm.exceptions import UnsupportedProviderError


SUPPORTED_PROVIDERS = {"mock", "gemini", "groq", "mistral"}


def get_llm_client(provider_name: str | None = None) -> LLMClient:
    """Return an LLM client for the selected provider.

    If provider_name is not provided, the default provider from settings is used.
    """
    selected_provider = (provider_name or settings.default_provider).lower()

    if selected_provider == "mock":
        return MockLLMClient()

    if selected_provider == "gemini":
        return GeminiClient()

    if selected_provider == "groq":
        return GroqClient()

    if selected_provider == "mistral":
        return MistralClient()

    raise UnsupportedProviderError(
        f"Unsupported provider: {selected_provider}. "
        f"Supported providers are: {sorted(SUPPORTED_PROVIDERS)}"
    )