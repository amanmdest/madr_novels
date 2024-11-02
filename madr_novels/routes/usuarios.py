from http import HTTPStatus

from fastapi import APIRouter

from madr_novels.schemas import (
    Mensagem,
    UsuarioEntrada,
    UsuarioSaida,
)

router = APIRouter(prefix='/usuarios', tags=['usuarios'])


@router.get('/home', status_code=HTTPStatus.OK, response_model=Mensagem)
def home():
    return {'mensagem': 'gracias a caetano por invitar-me'}


@router.post(
    '/conta', status_code=HTTPStatus.CREATED, response_model=UsuarioSaida
)
def criar_conta(usuario: UsuarioEntrada):
    return usuario
