from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from madr_novels.database import get_session
from madr_novels.models import Usuario
from madr_novels.schemas import (
    Mensagem,
    UsuarioEntrada,
    UsuarioLista,
    UsuarioSaida,
)
from madr_novels.security import get_password_hash

router = APIRouter(prefix='/usuarios', tags=['usuarios'])

T_Session = Annotated[Session, Depends(get_session)]


@router.get('/', response_model=UsuarioLista)
def usuarios(session: T_Session, limit: int = 10, skip: int = 0):
    usuario = session.scalars(select(Usuario).limit(limit).offset(skip))
    return {'usuarios': usuario}


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UsuarioSaida)
def criar_conta(usuario: UsuarioEntrada, session: T_Session):
    db_usuario = session.scalar(
        select(Usuario).where(
            or_(
                Usuario.username == usuario.username,
                Usuario.email == usuario.email,
            )
        )
    )

    if db_usuario:
        if db_usuario.username == usuario.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username já existe',
            )
        elif db_usuario.email == usuario.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email já está sendo utilizado',
            )

    usuario = Usuario(
        username=usuario.username,
        email=usuario.email,
        senha=get_password_hash(usuario.senha),
    )

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return usuario


# def usuario_por_id():


# def atualizar_conta():


@router.delete('/{usuario_id}', response_model=Mensagem)
def deletar_conta(usuario_id: int, session: T_Session):
    db_usuario = session.scalar(
        select(Usuario).where(Usuario.id == usuario_id)
    )

    if not db_usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuario não encontrado'
        )

    session.delete(db_usuario)
    session.commit()

    return {'mensagem': f'usuario {db_usuario.username} deletadao'}
