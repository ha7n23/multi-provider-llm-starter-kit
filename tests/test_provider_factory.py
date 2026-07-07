import pytest

from multi_provider_llm.clients.factory import SUPPORTED_PROVIDERS, get_llm_client
from multi_provider_llm.clients.mock_client import MockLLMClient
from multi_provider_llm.exceptions import UnsupportedProviderError


def test_supported_providers_contains_expected_values() -> None:
    assert SUPPORTED_PROVIDERS == {"mock", "gemini", "groq", "mistral"}


def test_factory_returns_mock_client() -> None:
    client = get_llm_client("mock")

    assert isinstance(client, MockLLMClient)


def test_factory_rejects_unsupported_provider() -> None:
    with pytest.raises(UnsupportedProviderError):
        get_llm_client("openai")