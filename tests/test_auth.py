from http import HTTPStatus


def test_login_acessar_token(cliente, usuario):
    response = cliente.post(
        '/token/',
        data={'username': usuario.email, 'password': usuario.chave_limpa},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'token_acesso' in token
    assert token['token_tipo'] == 'Bearer'


def test_login_email_errado(cliente, usuario):
    response = cliente.post(
        '/token/',
        data={
            'username': 'lotsofkanjis@ai.com',
            'password': usuario.chave_limpa,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email ou senha incorretos'}


def test_login_senha_errada(cliente, usuario):
    response = cliente.post(
        '/token/',
        data={
            'username': 'lotsofkanjis@ai.com',
            'password': usuario.chave_limpa,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email ou senha incorretos'}


def test_refresh_token(cliente, usuario, token):
    response = cliente.post(
        '/token/refresh_token', headers={'Authorization': f'Bearer {token}'}
    )
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'token_acesso' in data
    assert 'token_tipo' in data
    assert data['token_tipo'] == 'Bearer'
