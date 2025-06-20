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
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from madr_novels.database import get_session
from madr_novels.models import Usuario
from madr_novels.schemas import TokenData
from madr_novels.settings import Settings

T_Session = Annotated[Session, Depends(get_session)]

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


def pegar_usuario_autorizado(
    sessao: T_Session,
    token: str = Depends(oauth2_scheme),
):
    credenciais_invalidas = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Erro de validação de credenciais',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get('sub')
        if not username:
            raise credenciais_invalidas
        token_data = TokenData(username=username)
    except DecodeError:
        raise credenciais_invalidas

    except ExpiredSignatureError:
        raise credenciais_invalidas

    usuario = sessao.scalar(
        select(Usuario).where(Usuario.email == token_data.username)
    )

    if not usuario:
        raise credenciais_invalidas

    return usuario
