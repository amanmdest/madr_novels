import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from madr_novels.app import app
from madr_novels.models import table_registry


@pytest.fixture
def cliente():
    return TestClient(app)


@pytest.fixture
def sessao():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
