from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import (  # type: ignore
    DecodeError,
    ExpiredSignatureError,
    decode,
    encode,
)
from pwdlib import PasswordHash  # type: ignore
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from zoneinfo import ZoneInfo

from madr_novels.database import get_session
from madr_novels.models import Usuario
from madr_novels.settings import Settings

T_Sessao = Annotated[AsyncSession, Depends(get_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')
pwd_context = PasswordHash.recommended()
settings = Settings()


def senha_hash(senha: str):
    return pwd_context.hash(senha)


def verificar_senha(senha_crua: str, senha_hash: str):
    return pwd_context.verify(senha_crua, senha_hash)


def criando_token_de_acesso(data: dict):
    codificando = data.copy()

    expirar = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    codificando.update({'exp': expirar})

    jwt_codificado = encode(
        codificando, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return jwt_codificado


async def pegar_usuario_autorizado(
    sessao: T_Sessao,
    token: str = Depends(oauth2_scheme),
):
    credenciais_invalidas = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Erro de validação de credenciais',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
        subject_email = payload.get('sub')

        if not subject_email:
            raise credenciais_invalidas

    except DecodeError:
        raise credenciais_invalidas

    except ExpiredSignatureError:
        raise credenciais_invalidas

    usuario = await sessao.scalar(
        select(Usuario).where(Usuario.email == subject_email)
    )

    if not usuario:
        raise credenciais_invalidas

    return usuario
