from pydantic import BaseModel
from typing import List
from model.autor import Autor

class AutorSchema(BaseModel):
    """ Define como um novo autor a ser inserido deve ser representado """
    nome: str

class AutorViewSchema(BaseModel):
    """ Define como um autor será retornado: autor. """
    id: int
    nome: str

class AutorDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção. """
    message: str  # Corrigido "mesage" para "message"
    nome: str

class AutorBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será feita apenas com base no nome do autor. """
    nome: str

class ListagemAutoresSchema(BaseModel):
    """ Define como uma listagem de autores será retornada. """
    autores: List[AutorViewSchema]

def apresenta_autores(autores: List[Autor]):
    """ Retorna uma representação do autor seguindo o schema definido em AutorViewSchema. """
    result = []
    for autor in autores:
        result.append({
            "id": autor.id,
            "nome": autor.nome
        })

    return {"autores": result}

def apresenta_autor(autor: Autor):
    """ Retorna uma representação do autor seguindo o schema definido em AutorViewSchema. """
    return {
        "id": autor.id,
        "nome": autor.nome
    }