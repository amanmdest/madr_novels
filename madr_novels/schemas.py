from pydantic import BaseModel, ConfigDict, EmailStr


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
    # romancista_id: int # | None = None


class LivrosLista(BaseModel):
    livros: list[LivroSaida]


class LivroAtualizado(BaseModel):
    titulo: str
    ano: int


class RomancistaEntrada(BaseModel):
    nome: str


class RomancistaSaida(BaseModel):
    id: int
    nome: str
    livros: list[LivroSaida]


class RomancistasLista(BaseModel):
    romancistas: list[RomancistaSaida]


class RomancistaAtualizado(BaseModel):
    nome: str | None = None


class Token(BaseModel):
    token_acesso: str
    token_tipo: str


class TokenData(BaseModel):
    username: str | None = None


class FiltroPag(BaseModel):
    offset: int = 0
    limit: int = 100
