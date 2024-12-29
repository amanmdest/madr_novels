from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr_novels.database import get_session
from madr_novels.models import Romancista
from madr_novels.schemas import (
    RomancistaEntrada,
    RomancistaSaida,
    RomancistasLista,
)

router = APIRouter(prefix='/romancistas', tags=['romancistas'])

T_session = Annotated[Session, Depends(get_session)]


@router.get('/', status_code=HTTPStatus.OK, response_model=RomancistasLista)
def romancistas(session: T_session, limit: int = 10, skip: int = 0):
    romancistas = session.scalars(select(Romancista).limit(limit).offset(skip))
    return {'romancistas': romancistas}


@router.get(
    '/{romancista_id}',
    status_code=HTTPStatus.OK,
    response_model=RomancistaSaida,
)
def romancista_por_id(romancista_id: int, session: T_session):
    db_romancista = session.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )

    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='boogarins are you crazy?'
        )

    else:
        return {'romancista': db_romancista}


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=RomancistaSaida,
)
def novo_romancista(romancista: RomancistaEntrada, session: T_session):
    db_romancista = session.scalar(
        select(Romancista).where(Romancista.nome == romancista.nome)
    )

    if db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Romancista já se encontra cadastrado em nosso acervo! ;D',
        )

    romancista = Romancista(nome=romancista.nome)

    session.add(romancista)
    session.commit()
    session.refresh(romancista)

    return romancista


# def atualizar_romancista():


# def deletar_romancista():
