from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Mensagem(BaseModel):
    mensagem: str


class UsuarioEntrada(BaseModel):
    username: str
    email: EmailStr
    senha: str


class UsuarioSaida(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UsuarioLista(BaseModel):
    usuarios: list[UsuarioSaida]


class LivroEntrada(BaseModel):
    titulo: str
    ano: int
    romancista_id: int


class LivroSaida(BaseModel):
    id: int
    titulo: str
    ano: int
    romancista_id: int
    model_config = ConfigDict(from_attributes=True)


class LivrosLista(BaseModel):
    livros: list[LivroSaida]


class LivroAtualiza(BaseModel):
    titulo: str | None = None
    ano: int | None = None
    romancista_id: int | None = None


class RomancistaEntrada(BaseModel):
    nome: str


class RomancistaSaida(BaseModel):
    id: int
    nome: str
    livros: list[LivroSaida]
    model_config = ConfigDict(from_attributes=True)


class RomancistasLista(BaseModel):
    romancistas: list[RomancistaSaida]


class RomancistaAtualiza(BaseModel):
    nome: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class FiltroPag(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=10)
