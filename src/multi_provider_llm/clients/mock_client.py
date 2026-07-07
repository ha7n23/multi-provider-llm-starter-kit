from collections.abc import Iterator

from multi_provider_llm.exceptions import LLMProviderError

class MockLLMClient:
    """Mock LLM client for local development and tests.

    This client does not call any external API.
    It returns predictable responses so the app can be tested safely.
    """

    def generate(self, prompt:str) -> str:
        if not prompt.strip():
            raise LLMProviderError("Prompt cannot be empty")
        
        
        if "return ONLY valid JSON" in prompt:
            return """
            {
              "summary": "Customer reports a deducted QR payment that the merchant did not receive.",
              "category": "payment_dispute",
              "urgency": "high",
              "needs_human_review": true,
              "recommended_action": "Check transaction status and merchant settlement records."
            }
            """
        
        return (
            "This is a mock LLM response. In production, this would be generated "
            "by a real provider such as Gemini, Groq, or Mistral."
        )
    
    
    def generate_stream(self, prompt:str) -> Iterator[str]:
        response = self.generate(prompt)

        for word in response.split():
            yield word + " "