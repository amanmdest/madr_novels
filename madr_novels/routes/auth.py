from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr_novels.database import get_session
from madr_novels.models import Usuario
from madr_novels.schemas import Token
from madr_novels.security import (
    criando_token_de_acesso,
    pegar_usuario_autorizado,
    verificar_senha,
)

router = APIRouter(prefix='/auth', tags=['auth'])

T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
T_Session = Annotated[Session, Depends(get_session)]
T_UsuarioAutorizado = Annotated[Usuario, Depends(pegar_usuario_autorizado)]


@router.post('/token', response_model=Token)
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

    access_token = criando_token_de_acesso(data={'sub': usuario.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_token(usuario_autorizado: T_UsuarioAutorizado):
    novo_token = criando_token_de_acesso(
        data={'sub': usuario_autorizado.email}
    )

    return {'access_token': novo_token, 'token_type': 'Bearer'}
