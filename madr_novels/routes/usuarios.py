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
from madr_novels.security import (
    pegar_usuario_autorizado,
    senha_hash,
)

router = APIRouter(prefix='/usuarios', tags=['usuarios'])

T_UsuarioAutorizado = Annotated[Usuario, Depends(pegar_usuario_autorizado)]
T_Session = Annotated[Session, Depends(get_session)]


@router.get('/', response_model=UsuarioLista)
def usuarios(session: T_Session, limit: int = 10, skip: int = 0):
    usuarios = session.scalars(select(Usuario).limit(limit).offset(skip))
    return {'usuarios': usuarios}


@router.get('/{usuario_id}', response_model=UsuarioSaida)
def usuario_por_id(usuario_id: int, session: T_Session):
    usuario = session.scalar(select(Usuario).where(usuario_id == Usuario.id))
    return {'usuario': usuario}


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

    hash_senha = senha_hash(usuario.senha)

    db_usuario = Usuario(
        username=usuario.username,
        email=usuario.email,
        senha=hash_senha,
    )

    session.add(db_usuario)
    session.commit()
    session.refresh(db_usuario)

    return db_usuario


@router.put(
    '/{usuario_id}', status_code=HTTPStatus.OK, response_model=UsuarioSaida
)
def atualizar_conta(
    usuario: UsuarioEntrada,
    usuario_autorizado: T_UsuarioAutorizado,
    usuario_id: int,
    session: T_Session,
):
    if usuario_autorizado.id != usuario_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Você não possui as permissões esperadas pela aplicação.',
        )

    usuario_autorizado.email = usuario.email
    usuario_autorizado.username = usuario.username
    usuario_autorizado.senha = senha_hash(usuario.senha)

    session.add(usuario_autorizado)
    session.commit()
    session.refresh(usuario_autorizado)

    return usuario_autorizado


@router.delete(
    '/{usuario_id}', status_code=HTTPStatus.OK, response_model=Mensagem
)
def deletar_conta(
    usuario_autorizado: T_UsuarioAutorizado,
    usuario_id: int,
    session: T_Session,
):
    if usuario_autorizado.id != usuario_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Você não possui as permissões esperadas pela aplicação.',
        )

    session.delete(usuario_autorizado)
    session.commit()

    return {
        'mensagem': f'Usuário {usuario_autorizado.username} virou saudade.'
    }
