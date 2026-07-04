from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document
from app.schemas.document import DocumentCreate


def create_document(db: Session, document: DocumentCreate) -> Document:
    instance = Document(title=document.title, content=document.content)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def get_document_by_id(db: Session, document_id: int) -> Document | None:
    return db.get(Document, document_id)


def list_documents(db: Session) -> list[Document]:
    statement = select(Document)
    result = db.execute(statement)
    return list(result.scalars().all())
