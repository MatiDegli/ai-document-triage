import enum
from sqlalchemy import Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.models.document import Document


class CategoryEnum(str, enum.Enum):
    TECHNICAL = "technical"
    FINANCIAL = "financial"
    ACADEMIC = "academic"
    LEGAL = "legal"
    GENERAL = "general"


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    document_id: Mapped[int] = mapped_column(Integer, ForeignKey(Document.id))
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[CategoryEnum] = mapped_column(String, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"Analysis(id={self.document_id!r}, category={self.category!r})"
