from fastapi import FastAPI

from madr_novels.routes import livros, romancistas, usuarios

app = FastAPI(title='Madr')

app.include_router(usuarios.router)
app.include_router(romancistas.router)
app.include_router(livros.router)
