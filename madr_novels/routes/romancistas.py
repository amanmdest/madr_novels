from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr_novels.database import get_session
from madr_novels.models import Romancista
from madr_novels.schemas import RomancistaEntrada, RomancistaSaida

router = APIRouter(prefix='/romancistas', tags=['romancistas'])

T_session = Annotated[Session, Depends(get_session)]


@router.get('/', status_code=HTTPStatus.OK)
def romancistas(session: T_session, limit: int = 10, skip: int = 0):
    romancistas = session.scalars(select(Romancista).limit(limit).offset(skip))
    return {'romancistas': romancistas}


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=RomancistaSaida,
)
def adcionar_romancista(romancista: RomancistaEntrada):
    return romancista


# def romancista_por_id():


# def atualizar_romancista():


# def deletar_romancista():
