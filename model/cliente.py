from sqlalchemy import Column, String, Integer
from model import Base
from sqlalchemy.orm import relationship


class Cliente(Base):
    __tablename__ = 'cliente'
    id = Column("pk_cliente", Integer, primary_key=True)
    nome = Column(String(150), unique=True)
    agendamentos = relationship("Agendamento", cascade="all,delete",
                                back_populates="cliente")

    def __init__(self, nome: str):
        """
        Cria um cliente

        Argumentos:
            nome: nome do cliente.
        """
        self.nome = nome
