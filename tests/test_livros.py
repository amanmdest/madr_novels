from http import HTTPStatus

from madr_novels.schemas import LivroSaida


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
        'titulo': 'poesias reunidas',
        'ano': 1945,
        'romancista_id': 1,
    }


def test_novo_livro_campos_nao_preenchidos(cliente, romancista, token):
    response = cliente.post(
        '/livros/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'titulo': '',
            'ano': 1945,
            'romancista_id': romancista.id,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'É preciso preencher todos os campos'}


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


def test_listar_livros(cliente, livro, outro_livro):
    livro_schema = LivroSaida.model_validate(livro).model_dump()
    outro_livro_schema = LivroSaida.model_validate(outro_livro).model_dump()

    response = cliente.get('/livros/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'livros': [livro_schema, outro_livro_schema]}


def test_id_retornar_livro(cliente, livro):
    response = cliente.get('/livros/1')

    livro_schema = LivroSaida.model_validate(livro).model_dump()

    assert response.status_code == HTTPStatus.OK
    assert response.json() == livro_schema


def test_id_retornar_livro_nao_encontrado(cliente):
    response = cliente.get('/livros/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não encontrado no acervo'}


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
        'titulo': 'segunda fundação',
        'ano': 1942,
        'romancista_id': 1,
    }


def test_atualizar_livro_nao_encontrado(cliente, romancista, livro, token):
    response = cliente.patch(
        '/livros/10',
        json={
            'titulo': 'Segunda Fundação',
            'ano': 1942,
            'romancista_id': romancista.id,
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não encontrado no acervo'}


def test_atualizar_livro_romancista_nao_encontrado(
    cliente, romancista, livro, token
):
    response = cliente.patch(
        f'/livros/{livro.id}',
        json={'titulo': 'Segunda Fundação', 'ano': 1942, 'romancista_id': 2},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não encontrado no acervo'}


def test_deletar_livro(cliente, romancista, livro, token):
    response = cliente.delete(
        f'/livros/{livro.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'mensagem': f'Livro {livro.titulo} deletado do acervo'
    }


def test_deletar_livro_nao_encontrado(cliente, token):
    response = cliente.delete(
        '/livros/10', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não encontrado no acervo'}
