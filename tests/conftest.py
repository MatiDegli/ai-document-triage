import os
from collections.abc import Generator

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

from app.api.dependencies import get_llm_provider
from app.db.session import get_db
from app.llm.mock_provider import MockLLMProvider
from app.main import app

load_dotenv()

test_database_url = os.environ["TEST_DATABASE_URL"]
test_database_name = make_url(test_database_url).database

if test_database_name is None or not test_database_name.endswith("_test"):
    raise RuntimeError(
        "TEST_DATABASE_URL must point to a dedicated database ending in _test"
    )


test_engine = create_engine(test_database_url)
TestSessionLocal = sessionmaker(bind=test_engine)


def override_get_db() -> Generator[Session]:
    with TestSessionLocal() as db:
        yield db


def override_get_llm_provider() -> MockLLMProvider:
    return MockLLMProvider()


def clean_test_tables() -> None:
    with TestSessionLocal() as db:
        db.execute(text("TRUNCATE TABLE analyses, documents RESTART IDENTITY CASCADE"))
        db.commit()


@pytest.fixture(autouse=True)
def isolated_test_database() -> Generator[None]:
    app.dependency_overrides[get_db] = override_get_db
    clean_test_tables()

    try:
        yield
    finally:
        clean_test_tables()
        app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def mock_provider() -> Generator[None]:
    app.dependency_overrides[get_llm_provider] = override_get_llm_provider

    try:
        yield
    finally:
        app.dependency_overrides.pop(get_llm_provider, None)
