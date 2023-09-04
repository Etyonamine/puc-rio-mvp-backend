from sqlalchemy import Column, String, Integer, ForeignKey
from model import Base
from sqlalchemy.orm import relationship

    
class Modelo(Base):
    __tablename__ = 'modelo'
    cod_modelo = Column("pk_modelo", Integer, primary_key=True)
    nom_modelo = Column(String(100), unique=True)
    cod_marca = Column(Integer,
                         ForeignKey("marca.pk_marca"),
                        nullable=False)

    ## criar o vinculo com a marca do veiculo
    marca = relationship("Marca", back_populates="modelos")
    veiculos = relationship("Veiculo", back_populates="modelo")

    def __init__(self, nome: str, codigo_marca: Integer):
        """
        Cria uma modelo de veiculo de marca especifica

        Argumentos:
            nome: nome do modelo 
            cod_marca: codigo da marca
        """
        self.nom_modelo = nome
        self.cod_marca = codigo_marca
