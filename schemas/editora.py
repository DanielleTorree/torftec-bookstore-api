from pydantic import BaseModel
from typing import List
from model.editora import Editora

class EditoraSchema(BaseModel):
    """ Define como uma nova editora a ser inserida deve ser representada """
    nome: str

class EditoraViewSchema(BaseModel):
    """ Define como uma editora será retornada: editora. """
    id: int
    nome: str

class EditoraDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção. """
    message: str 
    nome: str

class EditoraBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será feita apenas com base no nome da editora. """
    nome: str

class ListagemEditorasSchema(BaseModel):
    """ Define como uma listagem de editoras será retornada. """
    editoras: List[EditoraViewSchema]

def apresenta_editoras(editoras: List[Editora]):
    """ Retorna uma representação da editora seguindo o schema definido em EditoraViewSchema. """
    result = []
    for editora in editoras:
        result.append({
            "id": editora.id,
            "nome": editora.nome
        })

    return {"editoras": result}

def apresenta_editora(editora: Editora):
    """ Retorna uma representação da editora seguindo o schema definido em EditoraViewSchema. """
    return {
        "id": editora.id,
        "nome": editora.nome
    }