from http import HTTPStatus

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


# def test_jwt_invalido(cliente):
#     response = cliente.delete(
#         '/usuarios/1',
#         headers={'Authorization': 'djxijxtchiguinguinn'},
#     )

#     assert response.status_code == HTTPStatus.UNAUTHORIZED
#     assert response.json() == {'detail': 'Erro de validação de credenciais.'}


def test_jwt_token_invalido(cliente):
    response = cliente.delete(
        '/usuarios/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Erro de validação de credenciais.'}
