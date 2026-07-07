import pytest

from multi_provider_llm.clients.mock_client import MockLLMClient
from multi_provider_llm.exceptions import LLMProviderError


def test_mock_client_generate_returns_text() -> None:
    client = MockLLMClient()

    response = client.generate("Explain LLM APIs.")

    assert isinstance(response, str)
    assert "mock LLM response" in response


def test_mock_client_rejects_empty_prompt() -> None:
    client = MockLLMClient()

    with pytest.raises(LLMProviderError):
        client.generate("")


def test_mock_client_streams_chunks() -> None:
    client = MockLLMClient()

    chunks = list(client.generate_stream("Explain streaming."))

    assert len(chunks) > 0
    assert all(isinstance(chunk, str) for chunk in chunks)