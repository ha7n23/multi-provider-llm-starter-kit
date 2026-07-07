import argparse
import logging
import sys

from multi_provider_llm.clients.factory import get_llm_client
from multi_provider_llm.config import settings
from multi_provider_llm.exceptions import LLMStarterKitError
from multi_provider_llm.services.complaint_service import ComplaintAnalysisService
from multi_provider_llm.utils.logging_config import setup_logging


logger = logging.getLogger(__name__)


DEFAULT_PROMPT = "Explain provider abstraction in 2 short bullet points."

DEFAULT_COMPLAINT = (
    "I made a QR payment and the amount was deducted from my account, "
    "but the merchant says they did not receive it."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the multi-provider LLM starter kit demo."
    )

    parser.add_argument(
        "--provider",
        choices=["mock", "gemini", "groq", "mistral"],
        default=settings.default_provider,
        help="LLM provider to use.",
    )

    parser.add_argument(
        "--prompt",
        default=DEFAULT_PROMPT,
        help="Prompt to send to the provider.",
    )

    parser.add_argument(
        "--stream",
        action="store_true",
        help="Stream the generated response.",
    )

    parser.add_argument(
        "--complaint",
        default=DEFAULT_COMPLAINT,
        help="Complaint text used for structured complaint analysis.",
    )

    parser.add_argument(
        "--analyse-complaint",
        action="store_true",
        help="Run structured complaint analysis instead of normal generation.",
    )

    return parser.parse_args()


def main() -> None:
    setup_logging()
    args = parse_args()

    logger.info("Starting demo.")
    logger.info("Selected provider: %s", args.provider)

    try:
        client = get_llm_client(args.provider)

        if args.analyse_complaint:
            service = ComplaintAnalysisService(llm_client=client)
            result = service.analyse_complaint(args.complaint)

            print("\nProvider:")
            print(args.provider)

            print("\nComplaint Analysis:")
            print(result.model_dump_json(indent=2))
            return

        print("\nProvider:")
        print(args.provider)

        print("\nPrompt:")
        print(args.prompt)

        if args.stream:
            print("\nStreaming Response:")
            for chunk in client.generate_stream(args.prompt):
                print(chunk, end="", flush=True)
            print()
            return

        response = client.generate(args.prompt)

        print("\nResponse:")
        print(response)

    except LLMStarterKitError as error:
        logger.error("Application error: %s", error)
        sys.exit(1)

    except Exception:
        logger.exception("Unexpected error occurred.")
        sys.exit(1)


if __name__ == "__main__":
    main()