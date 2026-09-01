"""Pydantic schemas for document API requests and responses."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.analysis import DocumentCategory


class AnalysisOutput(BaseModel):
    """Structured output returned by the document analysis provider."""

    summary: str = Field(min_length=1, max_length=2000)
    category: DocumentCategory
    confidence: float = Field(ge=0, le=1)


class AnalysisRead(AnalysisOutput):
    """Public representation of a persisted analysis."""

    id: int
    document_id: int
    provider: str
    model: str
    prompt_version: str = Field(pattern=r"^v\d{1,4}$")
    schema_version: str = Field(pattern=r"^v\d{1,4}$")
    latency_ms: float
    input_tokens: int | None = None
    output_tokens: int | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
