from http import HTTPStatus


def test_listar_livros(cliente):
    response = cliente.get('/livros/')

    response.status_code == HTTPStatus.OK
    response.json() == {'livros': []}


# def test_listar_livro_por_id(cliente):
#     response = cliente.get('/livros/{livro.id}')
#
#     response.status_code == HTTPStatus.OK
#     response.json() == {'livros': []}


def test_novo_livro(cliente, token):
    response = cliente.post(
        '/livros/',
        json={'titulo': 'Moby Dick', 'ano': 1851, 'romancista_id': 1},
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'titulo': 'Moby Dick',
        'ano': 1851,
        'romancista_id': 1,
    }


def test_livro_ja_cadastrado_no_acervo(cliente, livro, token):
    response = cliente.post(
        '/livros/',
        json={'titulo': livro.titulo, 'ano': 1851, 'romancista_id': 1},
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'Livro já cadastrado no acervo bb! ;D'
    }


def test_atualizar_livro(cliente, livro, token):
    response = cliente.put(
        f'/livros/{livro.id}',
        json={
            'titulo': 'As Mulheres de Tijucopapo',
            'ano': livro.ano,
            'romancista_id': livro.romancista_id,
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': livro.id,
        'titulo': livro.titulo,
        'ano': livro.ano,
        'romancista_id': livro.romancista_id,
    }


def test_deletar_livro(cliente, livro, token):
    response = cliente.delete(
        f'/livros/{livro.id}',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == f'Livro {livro.titulo} deletadao'
