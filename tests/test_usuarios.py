from http import HTTPStatus

from madr_novels.schemas import UsuarioSaida


def test_criar_conta(cliente):
    response = cliente.post(
        '/usuarios/',
        json={
            'username': 'jusant',
            'email': 'hermoso@juego.com',
            'senha': 'jusant',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'jusant',
        'email': 'hermoso@juego.com',
        'id': 1,
    }


def test_listar_usuarios(cliente):
    response = cliente.get('/usuarios/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'usuarios': []}


def test_listar_usuarios_com_usuario(cliente, usuario):
    usuario_schema = UsuarioSaida.model_validate(usuario).model_dump()
    response = cliente.get('/usuarios/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'usuarios': [usuario_schema]}


# def test_usuario_por_id(cliente, usuario):
#     response = cliente.get('/usuarios/1')
#     if 1 == usuario.id:
#         usuario_db = usuario
#
#     # usuario_schema = UsuarioSaida.model_validate(usuario_db).model_dump()
#
#     assert response.json() == {'usuario': [usuario_db]}


def test_criar_conta_username_repetido(cliente, usuario):
    response = cliente.post(
        '/usuarios/',
        json={
            'username': usuario.username,
            'email': 'pamonha@montanha.com',
            'senha': 'naosei',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username já existe'}


def test_criar_conta_email_repetido(cliente, usuario):
    response = cliente.post(
        '/usuarios/',
        json={
            'username': 'barril',
            'email': usuario.email,
            'senha': 'naosei',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email já está sendo utilizado'}


def test_atualizar_usuario(cliente, usuario, token):
    response = cliente.put(
        f'/usuarios/{usuario.id}',
        json={
            'username': 'barril',
            'email': 'latino@america.com',
            'senha': 'naosei',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': usuario.id,
        'username': 'barril',
        'email': 'latino@america.com',
    }


def test_atualizar_usuario_sem_autorizacao(
    cliente, usuario, outro_usuario, token
):
    response = cliente.put(
        f'/usuarios/{outro_usuario.id}',
        json={
            'username': 'barril',
            'email': 'latino@america.com',
            'senha': 'naosei',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'Você não possui as permissões esperadas pela aplicação'
    }


def test_deletar_usuario(cliente, usuario, token):
    response = cliente.delete(
        f'/usuarios/{usuario.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'mensagem': f'Usuário {usuario.username} virou saudade'
    }


def test_deletar_usuario_sem_autorizacao(
    cliente, usuario, outro_usuario, token
):
    response = cliente.delete(
        f'/usuarios/{outro_usuario.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'Você não possui as permissões esperadas pela aplicação'
    }
