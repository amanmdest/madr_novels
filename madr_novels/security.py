from datetime import datetime, timedelta

from jwt import encode  # type: ignore
from pwdlib import PasswordHash  # type: ignore
from zoneinfo import ZoneInfo

from madr_novels.settings import Settings

pwd_context = PasswordHash.recommended()


def senha_hash(senha: str):
    return pwd_context.hash(senha)


def verificar_senha(senha_crua: str, senha_hash: str):
    return pwd_context.verify(senha_crua, senha_hash)


def criando_token_de_acesso(data: dict):
    codificando = data.copy()

    expirar = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES
    )
    codificando.update({'exp': expirar})

    jwt_codificado = encode(
        codificando, Settings().SECRET_KEY, algorithm=Settings().ALGORITHM
    )

    return jwt_codificado
