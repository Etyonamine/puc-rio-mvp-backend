from sqlalchemy import Column, String , Integer
from model import Base

class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column("pk_cliente", Integer, primary_key=True)
    nome = Column(String(150), unique = True)

    def __init__(self, nome: str):
        """
        Cria um cliente

        Argumentos:
            nome: nome do cliente.
        """
        self.nome = nome