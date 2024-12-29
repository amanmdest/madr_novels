from http import HTTPStatus


def test_listar_livros(cliente):
    response = cliente.get('/livros/')

    response.status_code == HTTPStatus.OK
    response.json() == {'livros': []}


# def test_listar_livros(cliente):
#     response = cliente.get('/livros/')
#
#     response.status_code == HTTPStatus.OK
#     response.json() == {'livros': []}


def test_novo_livro(cliente):
    response = cliente.post(
        '/livros/',
        json={'titulo': 'Moby Dick', 'ano': 1851, 'romancista_id': 1},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'titulo': 'Moby Dick',
        'ano': 1851,
        'romancista_id': 1,
    }


def test_livro_ja_cadastrado_no_acervo(cliente):
    response = cliente.post(
        '/livros/',
        json={'titulo': 'Moby Dick', 'ano': 1851, 'romancista_id': 1},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.details == 'livro já cadastrado no acervo! ;D'
