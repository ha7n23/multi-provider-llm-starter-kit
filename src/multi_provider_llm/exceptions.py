class LLMStarterKitError(Exception):
    """Base class for exceptions in the LLM Starter Kit."""
    

class LLMProviderError(LLMStarterKitError):
    """Exception raised for errors related to LLM providers."""


class UnsupportedProviderError(LLMStarterKitError):
    """Exception raised when an unsupported LLM provider is specified."""


class StructuredOutputError(LLMStarterKitError):
    """Raised when structured output is invalid or cannot be parsed."""