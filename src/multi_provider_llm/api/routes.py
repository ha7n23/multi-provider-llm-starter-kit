from fastapi import APIRouter, HTTPException, status

from multi_provider_llm.api.schemas import (
    ComplaintAnalysisRequest,
    ComplaintAnalysisResponse,
    GenerateRequest,
    GenerateResponse,
    HealthResponse,
)
from multi_provider_llm.clients.factory import get_llm_client
from multi_provider_llm.config import settings
from multi_provider_llm.exceptions import LLMStarterKitError
from multi_provider_llm.services.complaint_service import ComplaintAnalysisService


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Return basic application health status."""
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        environment=settings.environment,
    )


@router.post("/generate", response_model=GenerateResponse)
def generate_text(request: GenerateRequest) -> GenerateResponse:
    """Generate text using the selected LLM provider."""
    try:
        client = get_llm_client(request.provider)
        response = client.generate(request.prompt)

        return GenerateResponse(
            provider=request.provider,
            response=response,
        )

    except LLMStarterKitError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.post("/complaints/analyse", response_model=ComplaintAnalysisResponse)
def analyse_complaint(
    request: ComplaintAnalysisRequest,
) -> ComplaintAnalysisResponse:
    """Analyse a banking complaint and return structured output."""
    try:
        client = get_llm_client(request.provider)
        service = ComplaintAnalysisService(llm_client=client)
        result = service.analyse_complaint(request.complaint)

        return ComplaintAnalysisResponse(
            provider=request.provider,
            summary=result.summary,
            category=result.category,
            urgency=result.urgency,
            needs_human_review=result.needs_human_review,
            recommended_action=result.recommended_action,
        )

    except LLMStarterKitError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error