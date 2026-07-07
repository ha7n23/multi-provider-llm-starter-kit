import json
from typing import Any

from pydantic import BaseModel

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
            raise StructuredOutputError("Complaint cannot be empty.")
        
        return COMPLAINT_TRIAGE_PROMPT.format(complaint=complaint)
    
    def analyse_complaint(self, complaint: str) -> ComplaintAnalysis:
        """Analyse a customer complaint and return structured output."""
        prompt = self.build_prompt(complaint)
        response_text = self.llm_client.generate(prompt)
        
        try:
            response_data: dict[str, Any] = json.loads(response_text)
            return ComplaintAnalysis(**response_data)
        except Exception as error:
            raise StructuredOutputError(
                f"Failed to parse complaint analysis JSON: {error}"
            ) from error