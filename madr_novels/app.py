from http import HTTPStatus

from fastapi import FastAPI

from madr_novels.routes import auth, livros, romancistas, usuarios
from madr_novels.schemas import Mensagem

app = FastAPI(title='MADR - Acervo Digital de Romancistas')

app.include_router(usuarios.router)
app.include_router(romancistas.router)
app.include_router(livros.router)
app.include_router(auth.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Mensagem)
def raiz():
    return {'mensagem': 'gracias a caetano por invitar-me!'}
