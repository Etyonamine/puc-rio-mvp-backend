from pydantic import BaseModel
from model.servico import Servico
from typing import List


class ServicoSchema(BaseModel):
    """Define com um novo serviço a ser inserido    """    
    descricao: str = "Corte de cabelo"
    valor: float = 10.00

class ServicoBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.Que será 
        feita apenas com base na descrição do serviço

    """
    descricao: str = "pintar a unha"

class ServicoBuscaDeleteSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
       Que será feita apenas com base no id do serviço

    """
    id: int = 1
class ServicoEditSchema(BaseModel):
    """ Define como editar um servico    """
    id: int = 1
    descricao: str = "Escova"
    valor: float = 10.00

class ListagemServicoSchema(BaseModel):
    """ Define como uma listagem de serviços que será retornada.    """
    servicos:List[ServicoSchema]

def apresenta_servicos(servicos: List[Servico]):    
    """ Retorna uma representação do servico seguido o schema definido em 
        ServicoViewSchema

    """
    result=[]
    for servico in servicos:
        result.append({
            "id": servico.id, 
            "descrição": servico.descricao,
            "valor": servico.valor
        })
    return {"serviços": result}
    
class ServicoViewSchema(BaseModel):
    """ Define como um serviço que será retornado: serviço. """
    id: int = 1
    descricao: str = "Corte masculino"
    valor: float = 10.00

class ServicoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.

    """
    message: str
    descricao: str

def apresenta_servico(servico: Servico):
    """  Retorna uma representação do serviço seguindo o schema definido em 
        ServicoViewSchema
        
    """
    return {       
        "id": servico.id,
        "descricao": servico.descricao,
        "valor": servico.valor
    }