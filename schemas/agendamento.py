from pydantic import BaseModel
from model.agendamento import Agendamento
from model.servico import Servico
from typing import List
from datetime import datetime

from model.cliente import Cliente


class AgendamentoSchema(BaseModel):
    """Define como um novo agendamento deve ser inserido """
    data_agenda: str = "01/01/2023 08:00:00"
    observacao: str = ""
    cliente_id: int = 1
    profissional_id: int = 1
    servico_id: int = 1


class AgendamentoBuscaIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com o codigo do agendamento

    """
    id: int = 1


class AgendamentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com o codigo do cliente e data de agendamento.

    """
    cliente_id: int = 1
    data_agenda: str = "01/04/2023 08:00:00"


class AgendamentoBuscaClienteSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com o codigo do cliente.

    """
    cliente_id: int = 1


class AgendamentoBuscaProfissionalSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com o codigo do profissional

    """
    profissional_id = 1


class AgendamentoBuscaServicoSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com o codigo do serviço

    """
    servico_id = 1


def apresenta_agendamentos(agendamentos: List[Agendamento]):
    """ Retorna uma representação do agendamento seguindo o schema definido em
        AgendamentoViewSchema.

    """
    result = []
    for agendamento in agendamentos:
        data_agenda= agendamento.data_agenda 
        result.append({
            "agenda_id": agendamento.id,
            "data_agenda": agendamento.data_agenda,
            "observacao": agendamento.observacao,
            "cliente_id": agendamento.cliente_id,
            "profissional_id": agendamento.profissional_id,
            "servico_id": agendamento.servico_id,
            "cliente": agendamento.cliente.nome,
            "profissional": agendamento.profissional.nome,
            "descricao_servico":  agendamento.servico.descricao,
            "valor_servico": agendamento.servico.valor
        })

    return {"agendamentos": result}


class AgendamentoViewSchema(BaseModel):
    """ Define como um agendamento será retornado """
    agenda_id: int = 1
    data_agenda: str = "2023-03-01 08:00:00"
    observacao: str = ""
    cliente_id: int = 1
    profissional_id: int = 1
    servico_id: int = 1
    cliente: str = "teste"
    profissional: str = "Carlos"
    descricao_servico: str = "teste"
    valor_servico: float = 0.00


class ListagemAgendamentoSchema(BaseModel):
    """ Define como uma listagem de agendamentos será retornada.
    """
    agendamentos: List[AgendamentoViewSchema]


class AgendamentoBuscaDelSchema(BaseModel):
    """ Define como a estrutura que representa a busca de delete.Que será
        feita apenas com o codigo do agendamento.

    """
    id: int = 1


class AgendamentoDelSchema(BaseModel):
    """ Define como deve ser a estrutura de recebimento
        para atualização do agendamento retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str


class AgendamentoEditSchema(BaseModel):
    """Define como será recebido os dados para a edição """
    id: int = 1
    data_agenda: str = '2023-01-01 08:00:00'
    cliente_id: int = 1
    profissional_id: int = 1
    servico_id: int = 1
    observacao: str = ''


def apresenta_agendamento(agendamento: Agendamento):
    """ Retorna uma representação do agendamento seguindo o schema definido em
        AgendamentoViewSchema.

    """
    return {
        "agenda_id": agendamento.id,
        "data_agenda": agendamento.data_agenda,
        "observacao": agendamento.observacao,
        "cliente_id": agendamento.cliente_id,
        "profissional_id": agendamento.profissional_id,
        "servico_id": agendamento.servico_id,
        "profissional": agendamento.profissional.nome,
        "cliente": agendamento.cliente.nome,
        "descricao_servico": agendamento.servico.descricao,
        "valor_servico": agendamento.servico.valor
    }
