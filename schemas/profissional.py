from pydantic import BaseModel
from model.profissional import Profissional
from typing import List
from model import Base


class ProfissionalSchema(BaseModel):
    """ Define com um novo profissional a ser inserido """
    id: int = 1
    nome: str = "Junior"


class ProfissionalBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.Que será
        feita apenas com base no nome do profissional

    """
    nome: str = "João"


class ClienteListaSchema(BaseModel):
    """Define como será o retorno das informações do profissional
       da ListagemProfissionalSchema

    """


class ProfissionalBuscaExclusaoSchema(BaseModel):
    """Define como será a estrutura que representa a busca.
       que será feita apenas com base no Id do profissional

    """
    id: int = 1


class ListagemProfissionalSchema(BaseModel):
    """Define como uma listagem de profissionais que será retornada. """
    profissionais: List[ClienteListaSchema]


def apresenta_profissionais(profissionais: List[Profissional]):
    """ Retorna uma representação do profissional seguido o schema definido em
        ProfissionalViewSchema

    """
    result = []
    for profissional in profissionais:
        result.append({
            "id": profissional.id,
            "nome": profissional.nome
        })
    return {"profissionais": result}


class ProfissionalViewSchema(BaseModel):
    """Define como um profissional que será retornado: profissional. """
    id: int = 1
    nome: str = "Junior"


class ProfissionalDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.

    """
    mesage: str
    nome: str


def apresenta_profissional(profissional: Profissional):
    """Retorna uma representação do profissional seguindo o schema definido em
       ProfissionalViewSchema

    """
    return {
        "id": profissional.id,
        "nome": profissional.nome
    }
