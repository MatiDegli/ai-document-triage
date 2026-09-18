from collections.abc import Sequence
from time import perf_counter

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.llm.provider import LLMProvider
from app.models.analysis import Analysis
from app.services.documents import get_document_by_id


def send_document_to_llm(
    db: Session,
    document_id: int,
    provider: LLMProvider,
) -> Analysis | None:
    document = get_document_by_id(db, document_id)

    if document is None:
        return None

    started_at = perf_counter()

    provider_result = provider.analyze(document)
    output = provider_result.output

    latency_ms = (perf_counter() - started_at) * 1000

    instance = Analysis(
        document_id=document.id,
        summary=output.summary,
        category=output.category,
        confidence=output.confidence,
        provider=provider.name,
        model=provider.model,
        prompt_version=provider.prompt_version,
        schema_version=provider.schema_version,
        latency_ms=latency_ms,
        input_tokens=provider_result.input_tokens,
        output_tokens=provider_result.output_tokens,
    )

    db.add(instance)
    db.commit()
    db.refresh(instance)

    return instance


def get_analyses_by_document_id(db: Session, document_id: int) -> Sequence[Analysis]:
    return db.scalars(select(Analysis).where(Analysis.document_id == document_id)).all()


def get_analysis_by_id(db: Session, analysis_id: int) -> Analysis | None:
    return db.get(Analysis, analysis_id)


def list_analyses(db: Session) -> list[Analysis]:
    statement = select(Analysis)
    result = db.execute(statement)
    return list(result.scalars().all())
