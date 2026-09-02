import os
from collections.abc import Generator

import pytest
from dotenv import load_dotenv
from sqlalchemy import text

from app.api.dependencies import get_llm_provider
from app.llm.mock_provider import MockLLMProvider
from app.main import app


load_dotenv()
os.environ["DATABASE_URL"] = os.environ["TEST_DATABASE_URL"]


@pytest.fixture(autouse=True)
def clean_documents_table() -> Generator[None, None, None]:
    from app.db.session import SessionLocal

    with SessionLocal() as db:
        db.execute(text("TRUNCATE TABLE analyses, documents RESTART IDENTITY CASCADE"))
        db.commit()

    yield

    with SessionLocal() as db:
        db.execute(text("TRUNCATE TABLE analyses, documents RESTART IDENTITY CASCADE"))
        db.commit()


def override_get_llm_provider() -> MockLLMProvider:
    return MockLLMProvider()


@pytest.fixture
def mock_provider() -> Generator[None, None, None]:
    app.dependency_overrides[get_llm_provider] = override_get_llm_provider

    yield

    app.dependency_overrides.pop(get_llm_provider, None)
