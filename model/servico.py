from sqlalchemy import Column, String , Integer, Float
from model import Base
from sqlalchemy.orm import relationship

class Servico(Base):
    __tablename__ = 'servico'

    id = Column("pk_servico", Integer, primary_key=True)
    descricao = Column(String(150), unique = True)
    valor = Column(Float)
    agendamentos = relationship("Agendamento",back_populates="servico")

    def __init__(self, descricao: str, valor: float):
        """
        Cria um servico

        Argumentos:
            descricao: descrição do servico
        """
        self.descricao = descricao
        self.valor = valor