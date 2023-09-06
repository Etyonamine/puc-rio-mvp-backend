from pydantic import BaseModel
from typing import List
from model import Base
from model.marca import Marca

class MarcaSchema(BaseModel):
    """Define como um novo registro de marca de veículo será inserido """
    codigo: int = 1
    nome: str = "GM"


class MarcaViewSchema(BaseModel):
    """ Define como uma marca de veículo deverá retornado: marca
    """
    codigo: int = 1
    nome: str = "GM"   


class MarcaEditSchema(BaseModel):
    """Define como será recebido os dados para a edição """
    codigo: int = 1
    nome: str = 'GM-EUA'    


class MarcaBuscaDelSchema(BaseModel):
    """ Define como a estrutura que representa a busca de delete.Que será
        feita apenas com o codigo da marca.

    """
    codigo: int = 1


class ListaMarcasSchema(BaseModel):
    """ Define como retorna a lista de marcas de veiculos.
    """
    marcas: List[MarcaViewSchema]


def apresenta_marca(marca: Marca):
    """ Retorna uma representação de um marca de veiculo seguindo o schema definido em
        MarcaViewSchema.
    """
    return {
        "codigo": marca.cod_marca,
        "nome": marca.nom_marca
    }



def apresenta_lista_marca(lista: List[Marca]):
    """ Retorna uma representação da marca de veiculo seguindo o schema definido em
        MarcaViewSchema.

    """
    result = []
    for item in lista:
       
        result.append({
            "codigo": item.cod_marca,
            "nome": item.nom_marca
        })

    return {"lista": result}    



