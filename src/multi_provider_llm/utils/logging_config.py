import logging

from multi_provider_llm.config import settings

def setup_logging() -> None:
    """Set up application logging.

    Logs should describe application behaviour, not secrets or sensitive data.
    """
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )