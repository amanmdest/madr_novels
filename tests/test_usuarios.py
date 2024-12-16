from http import HTTPStatus


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


def test_criar_conta_username_repetido(cliente):
    response = cliente.post(
        '/usuarios/',
        json={
            'username': 'jusant',
            'email': 'pamonha@montanha.com',
            'senha': 'naosei',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username já existe'}


def test_criar_conta_email_repetido(cliente):
    response = cliente.post(
        '/usuarios/',
        json={
            'username': 'barril',
            'email': 'hermoso@juego.com',
            'senha': 'naosei',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email já está sendo utilizado'}


def test_listar_usuarios(cliente):
    response = cliente.get('/usuarios/')

    assert response.status_code == HTTPStatus.OK
