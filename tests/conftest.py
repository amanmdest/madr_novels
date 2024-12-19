import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from madr_novels.app import app
from madr_novels.database import get_session
from madr_novels.models import Usuario, table_registry


@pytest.fixture
def cliente(sessao):
    def get_session_override():
        return sessao

    with TestClient(app) as cliente:
        app.dependency_overrides[get_session] = get_session_override
        yield cliente

    app.dependency_overrides.clear


@pytest.fixture
def sessao():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as sessao:
        yield sessao

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def usuario(sessao):
    usuario = Usuario(
        username='cienanosdesoledad',
        email='latino@america.com',
        senha='gabrielgarcia',
    )
    sessao.add(usuario)
    sessao.commit()
    sessao.refresh(usuario)

    return usuario
