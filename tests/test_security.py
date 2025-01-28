from http import HTTPStatus

from freezegun import freeze_time  # type: ignore
from jwt import decode  # type: ignore

from madr_novels.security import criando_token_de_acesso
from madr_novels.settings import Settings


def test_jwt():
    dados = {'sub': 'test@test.com'}
    token = criando_token_de_acesso(dados)

    decodificado = decode(
        token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM]
    )

    assert decodificado['sub'] == dados['sub']
    assert decodificado['exp']


def test_jwt_token_invalido(cliente):
    response = cliente.delete(
        '/usuarios/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Erro de validação de credenciais'}


def test_tempo_expiracao_jwt(cliente, usuario):
    with freeze_time('2023-07-14 12:00:00'):
        response = cliente.post(
            '/token/',
            data={'username': usuario.email, 'password': usuario.chave_limpa},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['token_acesso']

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
            '/token/',
            data={'username': usuario.email, 'password': usuario.chave_limpa},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['token_acesso']

    with freeze_time('2023-07-14 12:31:00'):
        response = cliente.post(
            '/token/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Erro de validação de credenciais'}
