import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
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
    romancista = Romancista(nome='Oswald de Andrade')

    sessao.add(romancista)
    await sessao.commit()
    await sessao.refresh(romancista)

    return romancista


@pytest_asyncio.fixture
async def outro_romancista(sessao):
    romancista = Romancista(nome='Marcelo Rubens Paiva')

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
