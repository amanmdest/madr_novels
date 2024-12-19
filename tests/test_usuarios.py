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


def test_usuarios(cliente):
    response = cliente.get('/usuarios/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'usuarios': []}


def test_usuarios_com_usuario(cliente, usuario):
    usuario_schema = UsuarioSaida.model_validate(usuario).model_dump()
    response = cliente.get('/usuarios/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'usuarios': [usuario_schema]}


def test_criar_conta_username_repetido(cliente, usuario):
    response = cliente.post(
        '/usuarios/',
        json={
            'username': 'cienanosdesoledad',
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
            'email': 'latino@america.com',
            'senha': 'naosei',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email já está sendo utilizado'}


def test_deletar_usuario(cliente, usuario):
    response = cliente.delete(f'/usuarios/{usuario.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'mensagem': f'usuario {usuario.username} deletadao'
    }
