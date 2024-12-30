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
from madr_novels.security import senha_hash

router = APIRouter(prefix='/usuarios', tags=['usuarios'])

T_Session = Annotated[Session, Depends(get_session)]


@router.get('/', response_model=UsuarioLista)
def usuarios(session: T_Session, limit: int = 10, skip: int = 0):
    usuario = session.scalars(select(Usuario).limit(limit).offset(skip))
    return {'usuarios': usuario}


# @router.get('/{usuario_id}', response_model=UsuarioSaida)
# def usuario_por_id():


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
        senha=senha_hash(usuario.senha),
    )

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return usuario


@router.put(
    '/{usuario_id}', status_code=HTTPStatus.OK, response_model=UsuarioSaida
)
def atualizar_conta(
    usuario_id: int,
    usuario: UsuarioEntrada,
    session: T_Session,
):
    db_usuario = session.scalar(
        select(Usuario).where(Usuario.id == usuario_id)
    )

    if not db_usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    db_usuario.email = usuario.email
    db_usuario.username = usuario.username
    db_usuario.senha = usuario.senha

    session.add(db_usuario)
    session.commit()
    session.refresh(db_usuario)

    return db_usuario


@router.delete(
    '/{usuario_id}', status_code=HTTPStatus.OK, response_model=Mensagem
)
def deletar_conta(usuario_id: int, session: T_Session):
    db_usuario = session.scalar(
        select(Usuario).where(Usuario.id == usuario_id)
    )

    if not db_usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    session.delete(db_usuario)
    session.commit()

    return {'mensagem': f'Usuário {db_usuario.username} deletadao'}
