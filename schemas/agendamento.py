 
from pydantic import BaseModel
from model.agendamento import Agendamento
from typing import List
from datetime import datetime

from model.cliente import Cliente

class AgendamentoSchema(BaseModel):
    """ Define como um novo agendamento deve ser inserido    
    """
    data_agenda: str = "01/04/2023 08:00:00"
    observacao: str = ""
    cliente_id: int = 1
    profissional_id: int = 1
    servico_id: int = 1


class AgendamentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com o codigo do cliente e data de agendamento.

    """
    cliente_id: int = 1
    data_agenda: str = "01/04/2023 08:00:00"



def apresenta_agendamentos(agendamentos: List[Agendamento]):
    """ Retorna uma representação do agendamento seguindo o schema definido em
        AgendamentoViewSchema.

    """
    result = []
    for agendamento in agendamentos:       
        result.append({
            "data_agenda": agendamento.data_agenda,
            "observacao": agendamento.observacao,
            "cliente_id": agendamento.cliente_id,
            "profissional_id": agendamento.profissional_id,
            "servico_id": agendamento.servico_id ,
            "cliente": agendamento.cliente.nome, 
            "profissional": agendamento.profissional.nome,
            "servico": agendamento.servico.descricao
        })

    return {"agendamentos": result}


class AgendamentoViewSchema(BaseModel):
    """ Define como um agendamento será retornado """
    data_agenda: str = "2023-03-01 08:00:00"
    observacao: str = ""
    cliente_id: int = 1
    profissional_id: int = 1
    servico_id: int = 1
    cliente: str = "teste"
    profissional: str = "Carlos"
    sevico: str = "corte de cabelo"
    
    
class ListagemAgendamentoSchema(BaseModel):
    """ Define como uma listagem de agendamentos será retornada.
    """
    agendamentos: List[AgendamentoViewSchema]    

class AgendamentoBuscaDelSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca de delete. Que será
        feita apenas com o codigo do agendamento.
        
    """
    id: int = 1

class AgendamentoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str


def apresenta_agendamento(agendamento: Agendamento):
    """ Retorna uma representação do agendamento seguindo o schema definido em
        AgendamentoViewSchema.

    """
    return {
        "id": agendamento.id,
        "data_agenda": agendamento.data_agenda,
        "observacao": agendamento.observacao,
        "cliente_id": agendamento.cliente_id,
        "profissional_id": agendamento.profissional_id,
        "servico_id": agendamento.servico_id         
    }
