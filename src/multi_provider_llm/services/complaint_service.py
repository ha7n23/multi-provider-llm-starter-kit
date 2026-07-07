import json
import re
from typing import Any

from pydantic import BaseModel, ValidationError

from multi_provider_llm.clients.base import LLMClient
from multi_provider_llm.exceptions import StructuredOutputError
from multi_provider_llm.prompts.complaint_prompts import COMPLAINT_TRIAGE_PROMPT


class ComplaintAnalysis(BaseModel):
    """Validated structure for complaint analysis output."""

    summary: str
    category: str
    urgency: str
    needs_human_review: bool
    recommended_action: str


class ComplaintAnalysisService:
    """Service for analysing customer complaints using an LLM client."""

    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    def build_prompt(self, complaint: str) -> str:
        if not complaint.strip():
            raise StructuredOutputError("Complaint text must not be empty.")

        return COMPLAINT_TRIAGE_PROMPT.format(complaint=complaint)

    def analyse_complaint(self, complaint: str) -> ComplaintAnalysis:
        prompt = self.build_prompt(complaint)
        response_text = self.llm_client.generate(prompt)

        return self.parse_analysis_response(response_text)

    def parse_analysis_response(self, response_text: str) -> ComplaintAnalysis:
        """Parse and validate an LLM complaint analysis response."""
        cleaned_response = self._clean_json_response(response_text)

        try:
            response_data: dict[str, Any] = json.loads(cleaned_response)
            return ComplaintAnalysis(**response_data)

        except json.JSONDecodeError as error:
            preview = cleaned_response[:500]
            raise StructuredOutputError(
                "Failed to parse complaint analysis JSON. "
                f"Parser error: {error}. "
                f"Response preview: {preview}"
            ) from error

        except ValidationError as error:
            raise StructuredOutputError(
                f"Complaint analysis response did not match expected schema: {error}"
            ) from error

    def _clean_json_response(self, response_text: str) -> str:
        """Clean common LLM JSON formatting issues.

        This handles cases where a model wraps JSON in markdown fences such as:
        ```json
        {...}
        ```
        """
        cleaned = response_text.strip()

        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?", "", cleaned.strip(), flags=re.IGNORECASE)
            cleaned = re.sub(r"```$", "", cleaned.strip())

        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start != -1 and end != -1 and end > start:
            cleaned = cleaned[start : end + 1]

        return cleaned.strip()