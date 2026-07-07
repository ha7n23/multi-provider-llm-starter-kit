import pytest

from multi_provider_llm.clients.mock_client import MockLLMClient
from multi_provider_llm.exceptions import StructuredOutputError
from multi_provider_llm.services.complaint_service import (
    ComplaintAnalysis,
    ComplaintAnalysisService,
)


def test_build_prompt_includes_complaint() -> None:
    service = ComplaintAnalysisService(llm_client=MockLLMClient())
    complaint = "My QR payment was deducted but the merchant did not receive it."

    prompt = service.build_prompt(complaint)

    assert complaint in prompt
    assert "return ONLY valid JSON" in prompt


def test_analyse_complaint_returns_valid_model() -> None:
    service = ComplaintAnalysisService(llm_client=MockLLMClient())

    result = service.analyse_complaint(
        "My QR payment was deducted but the merchant did not receive it."
    )

    assert isinstance(result, ComplaintAnalysis)
    assert result.category == "payment_dispute"
    assert result.urgency == "high"
    assert result.needs_human_review is True


def test_build_prompt_rejects_empty_complaint() -> None:
    service = ComplaintAnalysisService(llm_client=MockLLMClient())

    with pytest.raises(StructuredOutputError):
        service.build_prompt("")