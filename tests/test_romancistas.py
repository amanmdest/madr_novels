from http import HTTPStatus


def test_novo_romancista(cliente, token):
    response = cliente.post(
        '/romancistas/',
        json={'nome': 'Herman Melville'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    # assert response.json() == {
    #     'id': 1,
    #     'nome': 'Herman Melville',
    #     'livros': [
    #         {'id': 0, 'titulo': 'string', 'ano': 0, 'romancista_id': 0}
    #     ],
    # }


def test_romancista_ja_cadastrado_no_acervo(cliente, token, romancista):
    response = cliente.post(
        '/romancistas/',
        json={'nome': romancista.nome},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'Romancista já cadastrado no acervo bb! ;D'
    }


def test_listar_romancistas(cliente, romancista, outro_romancista):
    response = cliente.get('/romancistas/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'romancistas': [
            {'id': 1, 'livros': [], 'nome': 'Oswald de Andrade'},
            {'id': 2, 'livros': [], 'nome': 'Marcelo Rubens Paiva'},
        ]
    }


def test_id_retornar_romancista(cliente, romancista):
    response = cliente.get('/romancistas/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'livros': [],
        'nome': 'Oswald de Andrade',
    }


def test_id_retornar_romancista_nao_encontrado(cliente):
    response = cliente.get('/romancistas/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não encontrado no acervo'}


def test_atualizar_romancista(cliente, token, romancista):
    response = cliente.put(
        f'/romancistas/{romancista.id}',
        json={'nome': 'Clarice Lispector'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': romancista.id,
        'nome': romancista.nome,
        'livros': [],
    }


def test_atualizar_romancista_nao_encontrado(cliente, token):
    response = cliente.put(
        '/romancistas/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não encontrado no acervo'}


def test_deletar_romancista(cliente, romancista, token):
    response = cliente.delete(
        f'/romancistas/{romancista.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == f'Romancista {romancista.nome} deletado'


def test_deletar_romancista_nao_encontrado(cliente, token):
    response = cliente.delete(
        '/romancistas/10',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': '10 não encontrado no acervo'}
