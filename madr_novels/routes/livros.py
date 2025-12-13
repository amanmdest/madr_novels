from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from madr_novels.database import get_session
from madr_novels.models import Livro, Usuario
from madr_novels.schemas import (
    FiltroPag,
    LivroAtualizado,
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
T_Sessao = Annotated[AsyncSession, Depends(get_session)]
T_UsuarioAutorizado = Annotated[Usuario, Depends(pegar_usuario_autorizado)]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=LivroSaida,
)
async def novo_livro(
    livro: LivroEntrada,
    sessao: T_Sessao,
    usuario_autorizado: T_UsuarioAutorizado,
):
    livro.titulo = sanitiza_string(livro.titulo)

    if not livro.titulo or not livro.ano or not livro.romancista_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='É preciso preencher todos os campos',
        )

    await verifica_livro_existe_em_romancista(sessao, livro)
    await verifica_romancista_id_existe(sessao, livro)

    livro = Livro(
        titulo=livro.titulo,
        ano=livro.ano,
        romancista_id=livro.romancista_id,
    )

    sessao.add(livro)
    await sessao.commit()
    await sessao.refresh(livro)

    return livro


@router.get('/', status_code=HTTPStatus.OK, response_model=LivrosLista)
async def livros(filtro_pag: T_FiltroPag, sessao: T_Sessao):
    livros = await sessao.scalars(
        select(Livro).limit(filtro_pag.limit).offset(filtro_pag.offset)
    )
    return {'livros': livros}


@router.get(
    '/{livro_id}', status_code=HTTPStatus.OK, response_model=LivroSaida
)
async def livro_por_id(livro_id: int, sessao: T_Sessao):
    db_livro = await sessao.scalar(select(Livro).where(Livro.id == livro_id))

    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não encontrado no acervo',
        )

    return db_livro


@router.patch(
    '/{livro_id}', status_code=HTTPStatus.OK, response_model=LivroSaida
)
async def atualizar_livro(
    livro_id: int,
    livro: LivroAtualizado,
    sessao: T_Sessao,
    usuario_autorizado: T_UsuarioAutorizado,
):
    db_livro = await sessao.scalar(select(Livro).where(Livro.id == livro_id))

    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não encontrado no acervo',
        )

    await verifica_romancista_id_existe(sessao, livro)

    if livro.titulo:
        db_livro.titulo = sanitiza_string(livro.titulo)
    if livro.ano:
        db_livro.ano = livro.ano
    if livro.romancista_id:
        db_livro.romancista_id = livro.romancista_id

    await sessao.commit()
    await sessao.refresh(db_livro)

    return db_livro


@router.delete('/{livro_id}', response_model=Mensagem)
async def deletar_livro(
    livro_id: int, sessao: T_Sessao, usuario_autorizado: T_UsuarioAutorizado
):
    db_livro = await sessao.scalar(select(Livro).where(Livro.id == livro_id))

    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não encontrado no acervo',
        )

    await sessao.delete(db_livro)
    await sessao.commit()

    return {'mensagem': f'Livro {db_livro.titulo} deletado'}
