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
