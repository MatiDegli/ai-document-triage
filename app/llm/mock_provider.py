"""Deterministic mock provider for tests"""

from app.domain.analysis import DocumentCategory
from app.llm.provider import LLMProvider
from app.models.document import Document
from app.schemas.analysis import AnalysisOutput


class MockLLMProvider(LLMProvider):
    """Mock provider implementing the LLMProvider protocol."""

    name = "mock"
    model = "mock-v1"
    prompt_version = "v1"
    schema_version = "v1"

    def analyze(self, document: Document) -> AnalysisOutput:
        content = document.content

        matched_keyword: str | None = None

        category_map = {
            "python": DocumentCategory.TECHNICAL,
            "fastapi": DocumentCategory.TECHNICAL,
            "invoice": DocumentCategory.FINANCIAL,
            "budget": DocumentCategory.FINANCIAL,
            "study": DocumentCategory.ACADEMIC,
            "research": DocumentCategory.ACADEMIC,
            "law": DocumentCategory.LEGAL,
            "judge": DocumentCategory.LEGAL,
        }

        normalized_content = content.casefold()
        category: DocumentCategory | None = None

        for keyword, mapped_category in category_map.items():
            if keyword in normalized_content:
                category = mapped_category
                matched_keyword = keyword
                break

        if category is None:
            category = DocumentCategory.GENERAL

        excerpt = " ".join(normalized_content.split()[:20])

        if matched_keyword is not None:
            summary = f"Detected topic: {matched_keyword}. {excerpt}"
        elif excerpt:
            summary = excerpt
        else:
            summary = "No content provided."

        summary = summary[:2000].rstrip()

        if category is DocumentCategory.GENERAL:
            confidence = 0.5
        else:
            confidence = 0.9

        instance = AnalysisOutput(
            summary=summary, category=category, confidence=confidence
        )
        return instance
