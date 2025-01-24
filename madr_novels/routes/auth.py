from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr_novels.database import get_session
from madr_novels.models import Usuario
from madr_novels.schemas import Token
from madr_novels.security import criando_token_de_acesso, verificar_senha

router = APIRouter(prefix='/token', tags=['token'])

T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=Token)
def login_acessar_token(
    form_data: T_OAuth2Form,
    session: T_Session,
):
    usuario = session.scalar(
        select(Usuario).where(Usuario.email == form_data.username)
    )

    if not usuario or not verificar_senha(form_data.password, usuario.senha):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email ou senha incorretos',
        )

    token_acesso = criando_token_de_acesso(data={'sub': usuario.email})

    return {'token_acesso': token_acesso, 'token_tipo': 'Bearer'}
