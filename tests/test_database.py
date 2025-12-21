from dataclasses import asdict

import pytest
from sqlalchemy import select

from madr_novels.models import Livro, Romancista, Usuario


@pytest.mark.asyncio
async def test_criar_usuario(sessao, mock_db_time):
    with mock_db_time(model=Usuario) as time:
        novo_usuario = Usuario(
            username='aman', senha='1234', email='teste@teste.com'
        )
        sessao.add(novo_usuario)
        await sessao.commit()

        usuario = await sessao.scalar(
            select(Usuario).where(Usuario.username == 'aman')
        )

    assert asdict(usuario) == {
        'id': 1,
        'username': 'aman',
        'email': 'teste@teste.com',
        'senha': '1234',
        'created_at': time,
        'updated_at': time,
    }


@pytest.mark.asyncio
async def test_criar_romancista(sessao, mock_db_time):
    novo_romancista = Romancista(nome='Gabriel García Márquez')
    sessao.add(novo_romancista)
    await sessao.commit()

    romancista = await sessao.scalar(
        select(Romancista).where(Romancista.nome == 'Gabriel García Márquez')
    )

    assert asdict(romancista) == {
        'id': 1,
        'nome': 'Gabriel García Márquez',
        'livros': [],
    }


@pytest.mark.asyncio
async def test_criar_livro(sessao, romancista, mock_db_time):
    novo_livro = Livro(
        titulo='o rei da vela', ano='1933', romancista_id=romancista.id
    )
    sessao.add(novo_livro)
    await sessao.commit()

    livro = await sessao.scalar(
        select(Livro).where(Livro.titulo == 'o rei da vela')
    )

    assert asdict(livro) == {
        'id': 1,
        'titulo': 'o rei da vela',
        'ano': '1933',
        'romancista_id': romancista.id,
        'romancista': {'id': 1, 'livros': [], 'nome': 'oswald de andrade'},
    }


@pytest.mark.asyncio
async def test_romancista_livros_relationship(sessao, romancista, livro):
    await sessao.refresh(romancista)
    romancista = await sessao.scalar(
        select(Romancista).where(Romancista.id == romancista.id)
    )

    assert romancista.livros == [livro]
