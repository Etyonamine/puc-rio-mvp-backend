from pydantic import BaseModel
from model.cliente import Cliente
from typing import List
from model import Base


class ClienteSchema(BaseModel):
    """Define com um novo cliente a ser inserido """
    nome: str = "Junior"


class ClienteListaSchema(BaseModel):
    """Define como será o retorno do Cliente na listagem """
    id: int = 1
    nome: str = "Junior"


class ClienteBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.Que será
        feita apenas com base no nome do cliente

    """
    nome: str = "João"


class ClenteBuscaDeleteSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca
        para a remoção do cliente
    """
    id: int = 1


class ListagemClienteSchema(BaseModel):
    """ Define como uma listagem de clientes que será retornada."""
    clientes: List[ClienteListaSchema]


def apresenta_clientes(clientes: List[Cliente]):
    """ Retorna uma representação do cliente seguido o schema definido em
        ClienteViewSchema
    """
    result = []
    for cliente in clientes:
        result.append({
            "id": cliente.id,
            "nome": cliente.nome
        })
    return {"clientes": result}


class ClienteViewSchema(BaseModel):
    """ Define como um cliente que será retornado: cliente
    """
    id: int = 1
    nome: str = "Junior"


class ClienteDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str


def apresenta_cliente(cliente: Cliente):
    """Retorna uma representação do cliente seguindo o schema definido em
       ClienteViewSchema
    """
    return {
        "id": cliente.id,
        "nome": cliente.nome
    }
