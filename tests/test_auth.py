from http import HTTPStatus

from freezegun import freeze_time  # type: ignore


def test_login_acessar_token(cliente, usuario):
    response = cliente.post(
        '/auth/token/',
        data={'username': usuario.email, 'password': usuario.chave_limpa},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'Bearer'


def test_login_email_errado(cliente, usuario):
    response = cliente.post(
        '/auth/token/',
        data={
            'username': 'lotsofkanjis@ai.com',
            'password': usuario.chave_limpa,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email ou senha incorretos'}


def test_login_senha_errada(cliente, usuario):
    response = cliente.post(
        '/auth/token/',
        data={
            'username': 'lotsofkanjis@ai.com',
            'password': usuario.chave_limpa,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email ou senha incorretos'}


def test_refresh_token(cliente, token):
    response = cliente.post(
        '/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
    )
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'Bearer'


def test_tempo_expiracao_jwt(cliente, usuario):
    with freeze_time('2023-07-14 12:00:00'):
        response = cliente.post(
            '/auth/token/',
            data={'username': usuario.email, 'password': usuario.chave_limpa},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = cliente.put(
            f'/usuarios/{usuario.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'pacocaeruim',
                'email': 'masapalavra@elegal.com',
                'password': 'pacoca',
            },
        )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Erro de validação de credenciais'}


def test_tempo_expiracao_jwt_sem_refresh(cliente, usuario):
    with freeze_time('2023-07-14 12:00:00'):
        response = cliente.post(
            '/auth/token/',
            data={'username': usuario.email, 'password': usuario.chave_limpa},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = cliente.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Erro de validação de credenciais'}
