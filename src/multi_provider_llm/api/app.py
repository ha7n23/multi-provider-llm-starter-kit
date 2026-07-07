from fastapi import FastAPI

from multi_provider_llm.api.routes import router
from multi_provider_llm.config import settings
from multi_provider_llm.utils.logging_config import setup_logging


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    setup_logging()

    app = FastAPI(
        title=settings.app_name,
        description=(
            "A multi-provider LLM starter kit with provider abstraction, "
            "structured outputs, streaming support, and FastAPI endpoints."
        ),
        version="0.1.0",
    )

    app.include_router(router)

    return app


app = create_app()