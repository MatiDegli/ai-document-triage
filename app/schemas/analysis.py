"""Pydantic schemas for document API requests and responses."""

from typing import Literal
from pydantic import BaseModel, Field


class AnalysisOutput(BaseModel):
    """Public representation of a persisted analysis."""

    summary: str
    category: Literal["technical", "financial", "academic", "legal", "general"]
    confidence: float = Field(ge=0, le=1)
