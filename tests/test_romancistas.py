from http import HTTPStatus


def test_novo_romancista(cliente):
    response = cliente.post('/romancistas/', json={'nome': 'Herman Melville'})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'nome': 'Herman Melville',
        'livros': [],
    }


def test_romancista_ja_cadastrado_no_acervo(cliente, romancista):
    response = cliente.post('/romancistas/', json={'nome': romancista.nome})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'Romancista já cadastrado no acervo bb! ;D'
    }


def test_listar_romancistas(cliente):
    response = cliente.get('/romancistas/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'romancistas': []}


# def test_romancista_por_id(cliente, romancista):
#     response = cliente.get(f'/romancistas/{romancista.id}')
#
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {'romancista': romancista}


# def test_romancista_por_id_errado(cliente):
#     response = cliente.get('/romancistas/666')
#
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {'romancista': romancista}


def test_atualizar_romancista(cliente, romancista):
    response = cliente.put(
        f'/romancistas/{romancista.id}',
        json={'nome': 'Clarice Lispector'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': romancista.id,
        'nome': romancista.nome,
        'livros': [],
    }


def test_deletar_romancista(cliente, romancista):
    response = cliente.delete(
        f'/romancistas/{romancista.id}',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == f'Romancista {romancista.nome} deletadao'
