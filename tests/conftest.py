import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from madr_novels.app import app
from madr_novels.database import get_session
from madr_novels.models import table_registry
from madr_novels.security import senha_hash
from tests.factories import UsuarioFabrica


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture
def cliente(sessao):
    def get_session_override():
        return sessao

    with TestClient(app) as cliente:
        app.dependency_overrides[get_session] = get_session_override
        yield cliente

    app.dependency_overrides.clear


@pytest.fixture
def sessao(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as sessao:
        yield sessao

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def usuario(sessao):
    chave = 'avocado'

    usuario = UsuarioFabrica(senha=senha_hash(chave))
    sessao.add(usuario)
    sessao.commit()
    sessao.refresh(usuario)

    usuario.chave_limpa = 'avocado'

    return usuario


@pytest.fixture
def outro_usuario(sessao):
    chave = 'potato'

    usuario = UsuarioFabrica(senha=senha_hash(chave))

    sessao.add(usuario)
    sessao.commit()
    sessao.refresh(usuario)

    usuario.chave_limpa = 'potato'

    return usuario


# @pytest.fixture
# def romancista(sessao):
#     romancista = RomancistaFabrica()
#     sessao.add(romancista)
#     sessao.commit()
#     sessao.refresh(romancista)

#     return romancista


# @pytest.fixture
# def livro(sessao):
#     livro = LivroFabrica()
#     sessao.add(livro)
#     sessao.commit()
#     sessao.refresh(livro)

#     return livro


@pytest.fixture
def token(cliente, usuario):
    response = cliente.post(
        'auth/token/',
        data={'username': usuario.email, 'password': usuario.chave_limpa},
    )
    return response.json()['access_token']
