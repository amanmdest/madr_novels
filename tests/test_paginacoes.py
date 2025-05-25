from tests.fabricas import LivroFabrica, RomancistaFabrica


def test_paginacao_deve_retornar_cinco_romancistas(cliente, sessao, token):
    romancistas_esperados = 5
    sessao.bulk_save_objects(RomancistaFabrica.create_batch(5))
    sessao.commit()

    response = cliente.get(
        '/romancistas/?offset=0&limit=5',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['romancistas']) == romancistas_esperados


def test_paginacao_deve_retornar_dois_romancistas(cliente, sessao, token):
    romancistas_esperados = 2
    sessao.bulk_save_objects(RomancistaFabrica.create_batch(5))
    sessao.commit()

    response = cliente.get(
        '/romancistas/?offset=0&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['romancistas']) == romancistas_esperados


def test_paginacao_deve_retornar_cinco_livros(cliente, sessao, token):
    livros_esperados = 5
    sessao.bulk_save_objects(LivroFabrica.create_batch(5))
    sessao.commit()

    response = cliente.get(
        '/livros/?offset=0&limit=5',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['livros']) == livros_esperados


def test_paginacao_deve_retornar_dois_livros(cliente, sessao, token):
    livros_esperados = 2
    sessao.bulk_save_objects(LivroFabrica.create_batch(5))
    sessao.commit()

    response = cliente.get(
        '/livros/?offset=0&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['livros']) == livros_esperados
