from sqlalchemy import Column, String, Integer
from model import Base
from sqlalchemy.orm import relationship

class Marca(Base):
    __tablename__ = 'marca'
    cod_marca = Column("pk_marca", Integer, primary_key=True)
    nom_marca = Column(String(100), unique=True)

    ## criar o vinculo com os modelos do veiculo
    modelos = relationship("Modelo", cascade="all,delete",
                                back_populates="marca") 
    
    def __init__(self, nome: str):
        """
        Cria uma marca de veiculo

        Argumentos:
            nome: nome da marca
        """
        self.nom_marca = nome
