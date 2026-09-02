from typing import Sequence

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_llm_provider
from app.db.session import get_db
from app.llm.provider import LLMProvider
from app.models.analysis import Analysis
from app.models.document import Document
from app.schemas.analysis import AnalysisRead
from app.schemas.document import DocumentCreate, DocumentRead
from app.services.analyses import get_analyses_by_document_id, send_document_to_llm
from app.services.documents import create_document, get_document_by_id, list_documents


router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentRead, status_code=201)
def post_document(document: DocumentCreate, db: Session = Depends(get_db)) -> Document:
    instance = create_document(db, document)
    return instance


@router.get("", response_model=list[DocumentRead])
def get_documents_list(db: Session = Depends(get_db)) -> list[Document]:
    return list_documents(db)


@router.get("/{document_id}", response_model=DocumentRead)
def get_document(document_id: int, db: Session = Depends(get_db)) -> Document:
    document = get_document_by_id(db, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.get("/{document_id}/analyses", response_model=list[AnalysisRead])
def get_document_analyses(
    document_id: int, db: Session = Depends(get_db)
) -> Sequence[Analysis]:
    document = get_document_by_id(db, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return get_analyses_by_document_id(db, document_id)


@router.post("/{document_id}/analyze", response_model=AnalysisRead, status_code=201)
def analyze_document(
    document_id: int,
    db: Session = Depends(get_db),
    provider: LLMProvider = Depends(get_llm_provider),
) -> Analysis:
    analysis = send_document_to_llm(db, document_id, provider=provider)
    if analysis is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return analysis
