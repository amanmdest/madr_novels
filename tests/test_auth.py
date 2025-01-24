from http import HTTPStatus


def test_login_acessar_token(cliente, usuario):
    response = cliente.post(
        '/token/',
        data={'username': usuario.email, 'password': usuario.chave_limpa},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'token_acesso' in token
    assert token['token_tipo'] == "Bearer"
