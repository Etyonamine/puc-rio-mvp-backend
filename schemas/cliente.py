from pydantic import BaseModel
from model.cliente import Cliente
from typing import List


from  model import Base

class ClienteSchema(BaseModel):
    """ Define com um novo cliente a ser inserido
    """
    nome: str = "Junior"

class ClienteBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca.Que será 
        feita apenas com base no nome do cliente
    """
    nome: str = "João"


class ListagemClienteSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    clientes:List[ClienteSchema]

def apresenta_clientes(clientes: List[Cliente]):
    """ Retorna uma representação do produto seguido o schema definido em 
        ClienteViewSchema
    """
    result=[]
    for cliente in clientes:
        result.append({
            "nome": cliente.nome
        })
    return {"clientes": result}

class ClienteViewSchema(BaseModel):
    """ Define como um produto será retornado: produto + comentários.
    """
    id: int = 1
    nome: str = "Junior"

def apresenta_cliente(cliente: Cliente):
    """  Retorna uma representação do cliente seguindo o schema definido em 
        ClienteViewSchema
    """
    return {
        "id": cliente.id,
        "nome": cliente.nome
    }