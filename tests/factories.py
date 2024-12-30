import factory

from madr_novels.models import Livro, Romancista, Usuario


class UsuarioFabrica(factory.Factory):
    class Meta:
        model = Usuario

    username = factory.Sequence(lambda n: f'teste{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@madr.com')
    senha = factory.LazyAttribute(lambda obj: f'$#%{obj.username}$#%')


class RomancistaFabrica(factory.Factory):
    class Meta:
        model = Romancista

    nome = factory.Faker('name')


class LivroFabrica(factory.Factory):
    class Meta:
        model = Livro

    titulo = factory.Faker('sentence', nb_words=2)
    ano = factory.Faker('year')
    romancista_id = factory.Sequence(lambda n: n)
