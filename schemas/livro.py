from pydantic import BaseModel
from typing import List
from datetime import datetime
from model.livro import Livro


class LivroSchema(BaseModel):
    """ Define como um novo livro a ser inserido deve ser representado """
    titulo: str
    ano_publicacao: datetime
    id_editora: int
    ids_autores: List[int]


class LivroViewSchema(BaseModel):
    """ Define como um livro será retornado: livro. """
    id: int
    titulo: str
    ano_publicacao: int
    editora: str
    autores: List[str]


class LivroDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção. """
    message: str 
    titulo: str
    ano_publicacao: datetime


class LivroBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca, feita apenas com base no título do livro. """
    titulo: str


class ListagemLivrosSchema(BaseModel):
    """ Define como uma listagem de livros será retornada. """
    livros: List[LivroViewSchema]


def apresenta_livros(livros: List[Livro]):
    """ Retorna uma representação do livro seguindo o schema definido em LivroViewSchema. """
    result = []
    for livro in livros:
        result.append({
            "id": livro.id,
            "titulo": livro.titulo,
            "ano_publicacao": livro.ano_publicacao.year,  # Considerando exibir apenas o ano
            "editora": livro.editora.nome,
            "autores": [autor.nome for autor in livro.autores]
        })
    return {"livros": result}


def apresenta_livro(livro: Livro):
    """ Retorna uma representação do livro seguindo o schema definido em LivroViewSchema. """
    return {
        "id": livro.id,
        "titulo": livro.titulo,
        "ano_publicacao": livro.ano_publicacao.year,  # Considerando exibir apenas o ano
        "editora": livro.editora.nome,
        "autores": [autor.nome for autor in livro.autores]
    }
