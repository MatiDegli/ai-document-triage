from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentRead
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
