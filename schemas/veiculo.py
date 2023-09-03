from pydantic import BaseModel
from model.modelo import Modelo
from model.veiculo import Veiculo
from typing import List
from model import Base

class VeiculoSchema(BaseModel):
    """Define como um novo veiculo deve ser inserido """    
    placa: str = "ABC-1234"
    modelo_id: int = 1
   
class VeiculoViewSchema(BaseModel):
    """ Define como uma veículo deverá retornado: modelo
    """
    codigo: int = 1
    placa: str = "ABC-1234"   
    codigo_modelo: int = 30



class VeiculoEditSchema(BaseModel):
    """Define como será recebido os dados para a edição """
    codigo: int = 1
    placa: str = 'ABC-1235'    
    modelo_id: int = 30


class VeiculoBuscaDelSchema(BaseModel):
    """ Define como a estrutura que representa a busca de delete.Que será
        feita apenas com o codigo do agendamento.

    """
    codigo: int = 1


class ListaVeiculosSchema(BaseModel):
    """ Define como retorna a lista de veiculos.
    """
    agendamentos: List[VeiculoViewSchema]


def apresenta_veiculos(veiculo: Veiculo):
    """ Retorna uma representação de um veiculo seguindo o schema definido em
        MarcaViewSchema.
    """
    return {
        "codigo": veiculo.cod_veiculo,
        "nome": veiculo.des_placa,
        "codigo_modelo": veiculo.cod_modelo
    }



def apresenta_lista_veiculo(lista: List[Veiculo]):
    """ Retorna uma representação de veiculos seguindo o schema definido em
        VeiculoViewSchema.

    """
    result = []
    for item in lista:
       
        result.append({
            "codigo": item.cod_veiculo,
            "placa": item.des_placa,
            "codigo_modelo": item.cod_modelo

        })

    return {"lista": result}    


