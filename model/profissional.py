from sqlalchemy import Column, String , Integer
from model import Base
from sqlalchemy.orm import relationship

class Profissional(Base):
    __tablename__ = 'profissional'

    id = Column("pk_profissional", Integer, primary_key=True)
    nome = Column(String(150), unique = True)
    agendamentos = relationship("Agendamento", back_populates="profissional")

    def __init__(self, nome: str):
        """
        Cria um profissional

        Argumentos:
            nome: nome do profissional
        """
        self.nome = nome