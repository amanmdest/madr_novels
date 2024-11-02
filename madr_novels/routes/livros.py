from http import HTTPStatus

from fastapi import APIRouter

from madr_novels.schemas import LivroEntrada, LivroSaida

router = APIRouter(prefix='/livros', tags=['livros'])


@router.post(
    '/novo_livro',
    status_code=HTTPStatus.CREATED,
    response_model=LivroSaida,
)
def adcionar_livro(romancista: LivroEntrada):
    return romancista
