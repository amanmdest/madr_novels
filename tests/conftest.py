from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from madr_novels.app import app
from madr_novels.database import get_session
from madr_novels.models import Livro, Romancista, table_registry
from madr_novels.security import senha_hash
from tests.fabricas import UsuarioFabrica


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_async_engine(postgres.get_connection_url())
        yield _engine


@pytest.fixture
def cliente(sessao):
    def get_session_override():
        return sessao

    with TestClient(app) as cliente:
        app.dependency_overrides[get_session] = get_session_override
        yield cliente

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def sessao(engine):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as sessao:
        yield sessao

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 5, 20)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at') and hasattr(target, 'updated_at'):
            target.created_at = time
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def usuario(sessao):
    chave = 'avocado'

    usuario = UsuarioFabrica(senha=senha_hash(chave))
    sessao.add(usuario)
    await sessao.commit()
    await sessao.refresh(usuario)

    usuario.chave_limpa = 'avocado'

    return usuario


@pytest_asyncio.fixture
async def outro_usuario(sessao):
    chave = 'potato'

    usuario = UsuarioFabrica(senha=senha_hash(chave))

    sessao.add(usuario)
    await sessao.commit()
    await sessao.refresh(usuario)

    usuario.chave_limpa = 'potato'

    return usuario


@pytest_asyncio.fixture
async def romancista(sessao):
    romancista = Romancista(nome='oswald de andrade')

    sessao.add(romancista)
    await sessao.commit()
    await sessao.refresh(romancista)

    return romancista


@pytest_asyncio.fixture
async def outro_romancista(sessao):
    romancista = Romancista(nome='marcelo rubens paiva')

    sessao.add(romancista)
    await sessao.commit()
    await sessao.refresh(romancista)

    return romancista


@pytest_asyncio.fixture
async def livro(sessao, romancista):
    livro = Livro(
        titulo='o rei da vela', ano='1933', romancista_id=romancista.id
    )

    sessao.add(livro)
    await sessao.commit()
    await sessao.refresh(livro)

    return livro


@pytest_asyncio.fixture
async def outro_livro(sessao, romancista):
    livro = Livro(
        titulo='ainda estou aqui', ano='2015', romancista_id=romancista.id
    )

    sessao.add(livro)
    await sessao.commit()
    await sessao.refresh(livro)

    return livro


@pytest.fixture
def token(cliente, usuario):
    response = cliente.post(
        'auth/token/',
        data={'username': usuario.email, 'password': usuario.chave_limpa},
    )
    return response.json()['access_token']
