from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr_novels.database import get_session
from madr_novels.models import Romancista, Usuario
from madr_novels.schemas import (
    FiltroPag,
    RomancistaAtualiza,
    RomancistaEntrada,
    RomancistaSaida,
    RomancistasLista,
)
from madr_novels.security import pegar_usuario_autorizado

router = APIRouter(prefix='/romancistas', tags=['romancistas'])

T_FiltroPag = Annotated[FiltroPag, Query()]
T_Session = Annotated[Session, Depends(get_session)]
T_UsuarioAutorizado = Annotated[Usuario, Depends(pegar_usuario_autorizado)]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=RomancistaSaida,
)
def novo_romancista(
    romancista: RomancistaEntrada,
    sessao: T_Session,
    usuario_autorizado: T_UsuarioAutorizado,
):
    db_romancista = sessao.scalar(
        select(Romancista).where(Romancista.nome == romancista.nome)
    )

    if db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Romancista já cadastrado no acervo bb! ;D',
        )

    romancista = Romancista(nome=romancista.nome)

    sessao.add(romancista)
    sessao.commit()
    sessao.refresh(romancista)

    return romancista


@router.get('/', status_code=HTTPStatus.OK, response_model=RomancistasLista)
def romancistas(filtro_pag: T_FiltroPag, sessao: T_Session):
    romancistas = sessao.scalars(
        select(Romancista).limit(filtro_pag.limit).offset(filtro_pag.offset)
    )
    return {'romancistas': romancistas}


@router.get(
    '/{romancista_id}',
    status_code=HTTPStatus.OK,
    response_model=RomancistaSaida,
)
def romancista_por_id(romancista_id: int, sessao: T_Session):
    db_romancista = sessao.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )

    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não encontrado no acervo',
        )

    return db_romancista


@router.put(
    '/{romancista_id}',
    status_code=HTTPStatus.OK,
    response_model=RomancistaSaida,
)
def atualizar_romancista(
    romancista_id: int,
    romancista: RomancistaAtualiza,
    sessao: T_Session,
    usuario_autorizado: T_UsuarioAutorizado,
):
    db_romancista = sessao.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )

    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não encontrado no acervo',
        )

    db_romancista.nome = romancista.nome

    sessao.commit()
    sessao.refresh(db_romancista)

    return db_romancista


@router.delete('/{romancista_id}', status_code=HTTPStatus.OK)
def deletar_romancista(
    romancista_id: int,
    sessao: T_Session,
    usuario_autorizado: T_UsuarioAutorizado,
):
    db_romancista = sessao.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )

    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'{romancista_id} não encontrado no acervo',
        )

    sessao.delete(db_romancista)
    sessao.commit()  # TODO: author will be deleted with it's books ?

    return f'Romancista {db_romancista.nome} deletado'
