from typing import Protocol

from app.models.document import Document
from app.schemas.analysis import ProviderResult


class LLMProvider(Protocol):
    name: str
    model: str
    prompt_version: str
    schema_version: str

    def analyze(self, document: Document) -> ProviderResult: ...
