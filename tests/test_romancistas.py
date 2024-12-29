from http import HTTPStatus


def test_listar_romancistas(cliente):
    response = cliente.get('/romancistas/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'romancistas': []}


# def test_romancista_pelo_id(cliente):
#     response = cliente.get('/romancistas/{romancista_id}')
#
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {'romancista': romancista}


def test_novo_romancista(cliente):
    response = cliente.post('/romancistas/', json={'nome': 'Herman Melville'})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'nome': 'Herman Melville',
        'livros': [],
    }
