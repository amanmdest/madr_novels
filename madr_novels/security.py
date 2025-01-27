from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode  # type: ignore
from jwt.exceptions import PyJWTError  # type: ignore
from pwdlib import PasswordHash  # type: ignore
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from madr_novels.database import get_session
from madr_novels.models import Usuario

# from madr_novels.models import Usuario
# from madr_novels.schemas import TokenData
from madr_novels.settings import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = PasswordHash.recommended()
settings = Settings()

T_Session = Annotated[Session, Depends(get_session)]


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
    session: T_Session, token: str = Depends(oauth2_scheme)
):
    credenciais_invalidas = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Erro de validação de credenciais.',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get('sub')
        if not username:
            raise credenciais_invalidas

    except PyJWTError:
        raise credenciais_invalidas

    usuario = session.scalar(select(Usuario).where(Usuario.email == username))

    if not usuario:
        raise credenciais_invalidas

    return usuario
