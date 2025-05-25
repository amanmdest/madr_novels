from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr_novels.database import get_session
from madr_novels.models import Usuario
from madr_novels.schemas import (
    FiltroPag,
    Mensagem,
    UsuarioEntrada,
    UsuarioLista,
    UsuarioSaida,
)
from madr_novels.security import (
    pegar_usuario_autorizado,
    senha_hash,
)
from madr_novels.utils import verifica_usuario_existe

router = APIRouter(prefix='/usuarios', tags=['usuarios'])

T_FiltroPag = Annotated[FiltroPag, Query()]
T_Session = Annotated[Session, Depends(get_session)]
T_UsuarioAutorizado = Annotated[Usuario, Depends(pegar_usuario_autorizado)]


@router.get('/', response_model=UsuarioLista)
def usuarios(
    filtro_usuarios: T_FiltroPag,
    sessao: T_Session,
):
    usuarios = sessao.scalars(
        select(Usuario)
        .limit(filtro_usuarios.limit)
        .offset(filtro_usuarios.offset)
    )
    return {'usuarios': usuarios}


@router.get(
    '/{usuario_id}', status_code=HTTPStatus.OK, response_model=UsuarioSaida
)
def usuario_por_id(usuario_id: int, sessao: T_Session):
    usuario = sessao.scalar(select(Usuario).where(usuario_id == Usuario.id))

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado',
        )

    return usuario


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UsuarioSaida)
def criar_conta(usuario: UsuarioEntrada, sessao: T_Session):
    # if (
    #     usuario.username
    #     != sanitiza_string(usuario.username) or usuario.email
    #     != sanitiza_string(usuario.email)
    # ):
    #     raise HTTPException(
    #         status_code=HTTPStatus.BAD_REQUEST, detail='Melhorar formatação'
    #     ) # TODO

    verifica_usuario_existe(sessao, usuario)
    hash_senha = senha_hash(usuario.senha)

    db_usuario = Usuario(
        username=usuario.username,
        email=usuario.email,
        senha=hash_senha,
    )

    sessao.add(db_usuario)
    sessao.commit()
    sessao.refresh(db_usuario)

    return db_usuario


@router.put(
    '/{usuario_id}', status_code=HTTPStatus.OK, response_model=UsuarioSaida
)
def atualizar_conta(
    usuario: UsuarioEntrada,
    usuario_autorizado: T_UsuarioAutorizado,
    usuario_id: int,
    sessao: T_Session,
):
    if usuario_autorizado.id != usuario_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não possui as permissões esperadas pela aplicação',
        )

    usuario_autorizado.email = usuario.email
    usuario_autorizado.username = usuario.username
    usuario_autorizado.senha = senha_hash(usuario.senha)

    sessao.commit()
    sessao.refresh(usuario_autorizado)

    return usuario_autorizado


@router.delete(
    '/{usuario_id}', status_code=HTTPStatus.OK, response_model=Mensagem
)
def deletar_conta(
    usuario_autorizado: T_UsuarioAutorizado,
    usuario_id: int,
    sessao: T_Session,
):
    if usuario_autorizado.id != usuario_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não possui as permissões esperadas pela aplicação',
        )

    sessao.delete(usuario_autorizado)
    sessao.commit()

    return {'mensagem': f'Usuário {usuario_autorizado.username} virou saudade'}
