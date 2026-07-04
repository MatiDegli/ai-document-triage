import os
from collections.abc import Generator

import pytest
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()
os.environ["DATABASE_URL"] = os.environ["TEST_DATABASE_URL"]


@pytest.fixture(autouse=True)
def clean_documents_table() -> Generator[None, None, None]:
    from app.db.session import SessionLocal

    with SessionLocal() as db:
        db.execute(text("TRUNCATE TABLE documents RESTART IDENTITY CASCADE"))
        db.commit()

    yield

    with SessionLocal() as db:
        db.execute(text("TRUNCATE TABLE documents RESTART IDENTITY CASCADE"))
        db.commit()
