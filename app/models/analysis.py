"""SQLAlchemy model for persisted document analyses."""

from datetime import datetime

from sqlalchemy import (
    TIMESTAMP,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy import (
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.domain.analysis import DocumentCategory


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    document_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("documents.id"), nullable=False
    )
    summary: Mapped[str] = mapped_column(String(2000), nullable=False)
    category: Mapped[DocumentCategory] = mapped_column(
        SQLAlchemyEnum(
            DocumentCategory,
            name="document_category",
            values_callable=lambda enum_class: [  # pyright: ignore[reportUnknownLambdaType]
                member.value  # pyright: ignore[reportUnknownMemberType]
                for member in enum_class  # pyright: ignore[reportUnknownVariableType]
            ],
        ),
        nullable=False,
    )
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    prompt_version: Mapped[str] = mapped_column(String(5), nullable=False)
    schema_version: Mapped[str] = mapped_column(String(5), nullable=False)
    latency_ms: Mapped[float] = mapped_column(Float, nullable=False)
    input_tokens: Mapped[int | None] = mapped_column(Integer)
    output_tokens: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"Analysis(id={self.id!r}, document_id={self.document_id!r}, category={self.category!r})"
