from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr_novels.database import get_session
from madr_novels.models import Livro
from madr_novels.schemas import LivroEntrada, LivroSaida, LivrosLista

router = APIRouter(prefix='/livros', tags=['livros'])

T_session = Annotated[Session, Depends(get_session)]


@router.get('/', response_model=LivrosLista)
def livros(session: T_session, limit: int = 10, skip: int = 0):
    livros = session.scalars(select(Livro).limit(limit).offset(skip))
    return {'livros': livros}


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=LivroSaida,
)
def novo_livro(livro: LivroEntrada, session: T_session):
    db_livro = session.scalar(
        select(Livro).where(Livro.titulo == livro.titulo)
    )

    if db_livro:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            details='Livro já cadastrado no acervo! ;D',
        )

    livro = Livro(
        titulo=livro.titulo, ano=livro.ano, romancista_id=livro.romancista_id
    )

    session.add(livro)
    session.commit()
    session.refresh(livro)

    return livro


# def livro_por_id():


# def atualizar_livro():


# def deletar_livro():
