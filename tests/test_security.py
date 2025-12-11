from http import HTTPStatus

import jwt
import pytest  # type: ignore
from fastapi import HTTPException
from jwt import decode

from madr_novels.security import (
    criando_token_de_acesso,
    pegar_usuario_autorizado,
    settings,
)


def test_jwt():
    dados = {'sub': 'test@test.com'}
    token = criando_token_de_acesso(dados)

    decodificado = decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

    assert decodificado['sub'] == dados['sub']
    assert decodificado['exp']


def test_jwt_token_invalido(cliente):
    response = cliente.delete(
        '/usuarios/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Erro de validação de credenciais'}


@pytest.mark.asyncio
async def test_pegar_usuario_sem_sub(sessao):
    token = criando_token_de_acesso(data={'test': 'test'})
    with pytest.raises(HTTPException) as exc:
        await pegar_usuario_autorizado(sessao=sessao, token=token)

    assert exc.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exc.value.detail == 'Erro de validação de credenciais'


@pytest.mark.asyncio
async def test_user_nao_encontrado_no_bd(sessao):
    token = jwt.encode(
        {'sub': 'JurassicPark'},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    with pytest.raises(HTTPException) as excinfo:
        await pegar_usuario_autorizado(sessao=sessao, token=token)

    assert excinfo.value.status_code == HTTPStatus.UNAUTHORIZED
    assert excinfo.value.detail == 'Erro de validação de credenciais'
