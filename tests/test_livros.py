from http import HTTPStatus


def test_listar_livros(cliente):
    response = cliente.get('/livros/')

    response.status_code == HTTPStatus.OK
    response.json() == {'livros': []}


# def test_novo_livro_em_romancista_db_relationship(romancista, session):
#     livro = LivroFabrica()

#     session.add(livro)
#     session.commit()
#     session.refresh(livro)

#     romancista = session.scalar(
#       select(Romancista).where(Romancista.id == livro.romancista_id)
#     )

#     assert livro in romancista.livros


# def test_listar_livro_por_id(cliente):
#     response = cliente.get('/livros/{livro.id}')
#
#     response.status_code == HTTPStatus.OK
#     response.json() == {'livros': []}


def test_novo_livro(cliente, romancista, token):
    response = cliente.post(
        '/livros/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'titulo': 'Poesias Reunidas',
            'ano': 1945,
            'romancista_id': romancista.id,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'titulo': 'Poesias Reunidas',
        'ano': 1945,
        'romancista_id': 1,
    }


def test_livro_ja_cadastrado_no_acervo(cliente, romancista, livro, token):
    response = cliente.post(
        '/livros/',
        json={
            'titulo': livro.titulo,
            'ano': 1851,
            'romancista_id': romancista.id,
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'Livro já cadastrado no acervo bb! ;D'
    }


def test_atualizar_livro(cliente, romancista, livro, token):
    response = cliente.patch(
        f'/livros/{livro.id}',
        json={
            'titulo': 'Segunda Fundação',
            'ano': 1942,
            'romancista_id': romancista.id,
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': livro.id,
        'titulo': 'Segunda Fundação',
        'ano': 1942,
        'romancista_id': 1,
    }


def test_atualizar_livro_nao_encontrado(cliente, token):
    response = cliente.patch(
        '/livros/10', json={}, headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não encontrado no acervo.'}


def test_deletar_livro(cliente, romancista, livro, token):
    response = cliente.delete(
        f'/livros/{livro.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'mensagem': f'Livro {livro.titulo} deletadao'}
