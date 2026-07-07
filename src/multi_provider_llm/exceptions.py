class LLMStarterKitError(Exception):
    """Base exception for the LLM starter kit."""


class LLMProviderError(LLMStarterKitError):
    """Raised when an LLM provider fails."""


class MissingAPIKeyError(LLMStarterKitError):
    """Raised when a required API key is missing."""


class UnsupportedProviderError(LLMStarterKitError):
    """Raised when a selected provider is not supported."""


class StructuredOutputError(LLMStarterKitError):
    """Raised when structured output is invalid or cannot be parsed."""