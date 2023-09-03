from pydantic import BaseModel
from model.modelo import Modelo
from model.marca import Marca
from typing import List
from model import Base


class ModeloSchema(BaseModel):
    """Define como um novo registro de modelo de veículo será inserido """
    codigo: int = 1
    nome: str = "GM"


class ModeloViewSchema(BaseModel):
    """ Define como uma modelo de veículo deverá retornado: modelo
    """
    codigo: int = 1
    nome: str = "GM"   


class ModeloEditSchema(BaseModel):
    """Define como será recebido os dados para a edição """
    codigo: int = 1
    nome: str = 'GM-EUA'    


class ModeloBuscaDelSchema(BaseModel):
    """ Define como a estrutura que representa a busca de delete.Que será
        feita apenas com o codigo do agendamento.

    """
    codigo: int = 1


class ListaModelosSchema(BaseModel):
    """ Define como retorna a lista de marcas de veiculos.
    """
    agendamentos: List[ModeloViewSchema]


def apresenta_modelo(modelo: Modelo):
    """ Retorna uma representação de um modelo de veiculo seguindo o schema definido em
        MarcaViewSchema.
    """
    return {
        "codigo": modelo.cod_marca,
        "nome": modelo.nom_marca
    }



def apresenta_lista_modelo(lista: List[Modelo]):
    """ Retorna uma representação do agendamento seguindo o schema definido em
        ModeloViewSchema.

    """
    result = []
    for item in lista:
       
        result.append({
            "codigo": item.cod_marca,
            "nome": item.nom_marca
        })

    return {"lista": result}    



