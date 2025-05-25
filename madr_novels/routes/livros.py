from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr_novels.database import get_session
from madr_novels.models import Livro, Usuario
from madr_novels.schemas import (
    FiltroPag,
    LivroAtualiza,
    LivroEntrada,
    LivroSaida,
    LivrosLista,
    Mensagem,
)
from madr_novels.security import pegar_usuario_autorizado
from madr_novels.utils import (
    sanitiza_string,
    verifica_livro_existe_em_romancista,
    verifica_romancista_id_existe,
)

router = APIRouter(prefix='/livros', tags=['livros'])

T_FiltroPag = Annotated[FiltroPag, Query()]
T_Session = Annotated[Session, Depends(get_session)]
T_UsuarioAutorizado = Annotated[Usuario, Depends(pegar_usuario_autorizado)]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=LivroSaida,
)
def novo_livro(
    livro: LivroEntrada,
    sessao: T_Session,
    usuario_autorizado: T_UsuarioAutorizado,
):
    verifica_livro_existe_em_romancista(sessao, livro)
    verifica_romancista_id_existe(sessao, livro)

    if (
        not sanitiza_string(livro.titulo)
        or not livro.ano
        or not livro.romancista_id
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='É preciso preencher todos os campos',
        )

    livro = Livro(
        titulo=sanitiza_string(livro.titulo),
        ano=livro.ano,
        romancista_id=livro.romancista_id,
    )

    sessao.add(livro)
    sessao.commit()
    sessao.refresh(livro)

    return livro


@router.get('/', status_code=HTTPStatus.OK, response_model=LivrosLista)
def livros(filtro_pag: T_FiltroPag, sessao: T_Session):
    livros = sessao.scalars(
        select(Livro).limit(filtro_pag.limit).offset(filtro_pag.offset)
    )
    return {'livros': livros}


@router.get(
    '/{livro_id}', status_code=HTTPStatus.OK, response_model=LivroSaida
)
def livro_por_id(livro_id: int, sessao: T_Session):
    db_livro = sessao.scalar(select(Livro).where(Livro.id == livro_id))

    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não encontrado no acervo',
        )

    return db_livro


@router.patch(
    '/{livro_id}', status_code=HTTPStatus.OK, response_model=LivroSaida
)
def atualizar_livro(
    livro_id: int,
    livro: LivroAtualiza,
    sessao: T_Session,
    usuario_autorizado: T_UsuarioAutorizado,
):
    db_livro = sessao.scalar(select(Livro).where(Livro.id == livro_id))

    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não encontrado no acervo',
        )

    verifica_romancista_id_existe(sessao, livro)

    if livro.titulo:
        db_livro.titulo = sanitiza_string(livro.titulo)
    if livro.ano:
        db_livro.ano = livro.ano
    if livro.romancista_id:
        db_livro.romancista_id = livro.romancista_id

    sessao.commit()
    sessao.refresh(db_livro)

    return db_livro


@router.delete('/{livro_id}', response_model=Mensagem)
def deletar_livro(
    livro_id: int, sessao: T_Session, usuario_autorizado: T_UsuarioAutorizado
):
    db_livro = sessao.scalar(select(Livro).where(Livro.id == livro_id))

    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não encontrado no acervo',
        )

    sessao.delete(db_livro)
    sessao.commit()

    return {'mensagem': f'Livro {db_livro.titulo} deletadao'}
