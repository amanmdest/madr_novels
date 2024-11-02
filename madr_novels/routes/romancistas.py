from http import HTTPStatus

from fastapi import APIRouter

from madr_novels.schemas import RomancistaEntrada, RomancistaSaida, UsuarioDB

router = APIRouter(prefix='/romancistas', tags=['romancistas'])


@router.post(
    '/novo_romancista',
    status_code=HTTPStatus.CREATED,
    response_model=RomancistaSaida,
)
def adcionar_romancista(romancista: RomancistaEntrada):
    return romancista
