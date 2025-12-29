import asyncio

import pytest

from tests.fabricas import LivroFabrica, RomancistaFabrica


@pytest.mark.asyncio
async def test_listar_romancistas_paginacao_deve_retornar_dois_romancistas(
    cliente, sessao
):
    romancistas_esperados = 2
    sessao.add_all(RomancistaFabrica.create_batch(5))
    await sessao.commit()

    response = cliente.get('/romancistas/?offset=0&limit=2')
    assert len(response.json()['romancistas']) == romancistas_esperados


def test_listar_romancistas_paginacao_deve_retornar_cinco_romancistas(
    cliente, sessao
):
    romancistas_esperados = 5
    sessao.add_all(RomancistaFabrica.create_batch(5))
    asyncio.run(sessao.commit())

    response = cliente.get('/romancistas/?offset=0&limit=5')

    assert len(response.json()['romancistas']) == romancistas_esperados


def test_listar_livros_paginacao_deve_retornar_dois_livros(
    cliente, romancista, sessao
):
    livros_esperados = 2
    sessao.add_all(LivroFabrica.create_batch(5))
    asyncio.run(sessao.commit())

    response = cliente.get('/livros/?offset=2&limit=2')

    assert len(response.json()['livros']) == livros_esperados


def test_listar_romancistas_paginacao_deve_retornar_cinco_livros(
    cliente, romancista, sessao
):
    livros_esperados = 5
    sessao.add_all(LivroFabrica.create_batch(5))
    asyncio.run(sessao.commit())

    response = cliente.get('/livros/?offset=0&limit=5')

    assert len(response.json()['livros']) == livros_esperados
