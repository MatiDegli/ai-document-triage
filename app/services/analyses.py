from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.services.documents import get_document_by_id
from app.schemas.analysis import AnalysisOutput


def send_document_to_LLM(db: Session, document_id: int) -> Analysis | None:
    if (document := get_document_by_id(db, document_id)) is None:
        return None
    output = (AnalysisOutput) analyze(document)
    instance = Analysis(document_id=document_id, summary=output.summary, category=output.category, confidence=output.confidence)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def get_analyses_by_document_id(db: Session, document_id: int) -> Sequence[Analysis] | Analysis | None:
    return db.scalars(select(Analysis).where(Analysis.document_id == document_id)).all()


def get_analyses_by_id(db: Session, id: int) -> Analysis | None:
    return db.get(Analysis, id)
