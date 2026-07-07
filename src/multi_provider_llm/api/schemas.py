from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    app_name: str
    environment: str


class GenerateRequest(BaseModel):
    """Request body for normal text generation."""

    prompt: str = Field(..., min_length=1)
    provider: str = Field(default="mock", description="Provider: mock, gemini, groq, mistral")


class GenerateResponse(BaseModel):
    """Response body for normal text generation."""

    provider: str
    response: str


class ComplaintAnalysisRequest(BaseModel):
    """Request body for complaint analysis."""

    complaint: str = Field(..., min_length=1)
    provider: str = Field(default="mock", description="Provider: mock, gemini, groq, mistral")


class ComplaintAnalysisResponse(BaseModel):
    """Response body for structured complaint analysis."""

    provider: str
    summary: str
    category: str
    urgency: str
    needs_human_review: bool
    recommended_action: str