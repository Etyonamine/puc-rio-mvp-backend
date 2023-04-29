from sqlalchemy import Column, String, Integer, DateTime,\
                       ForeignKey, UniqueConstraint
from model import Base
from sqlalchemy.orm import relationship


class Agendamento(Base):
    __tablename__ = 'agendamento'
    __table_args__ = (
        UniqueConstraint('data_agenda', 'cliente_id',
                         'profissional_id', 'servico_id',
                         name='unique_agendamento_commit'),
    )
    id = Column("pk_agenda", Integer, primary_key=True)
    data_agenda = Column(DateTime)
    cliente_id = Column(Integer,
                        ForeignKey("cliente.pk_cliente"),
                        nullable=False)
    profissional_id = Column(Integer,
                             ForeignKey("profissional.pk_profissional"),
                             nullable=False)
    servico_id = Column(Integer, ForeignKey("servico.pk_servico"),
                        nullable=False)
    observacao = Column(String(300))

    cliente = relationship("Cliente", back_populates="agendamentos")
    profissional = relationship("Profissional", back_populates="agendamentos")
    servico = relationship("Servico", back_populates="agendamentos")

    def __init__(self, data_agenda: DateTime, cliente_id: int,
                 profissional_id: int, servico_id: int,
                 observacao: str):
        self.data_agenda = data_agenda
        self.cliente_id = cliente_id
        self.profissional_id = profissional_id
        self.servico_id = servico_id
        self.observacao = observacao
