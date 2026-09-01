"""Exceptions raised by LLM providers."""


class ProviderError(RuntimeError):
    """Raised when an LLM provider cannot return a usable response."""
