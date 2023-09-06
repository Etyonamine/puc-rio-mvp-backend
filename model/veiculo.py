from sqlalchemy import Column, String, Integer, ForeignKey
from model import Base
from sqlalchemy.orm import relationship


class Veiculo(Base):
    __tablename__ = 'veiculo'
    cod_veiculo = Column("pk_veiculo", Integer, primary_key=True)
    des_placa = Column(String(100), unique=True)
    cod_modelo = Column(Integer,
                         ForeignKey("modelo.pk_modelo"),
                        nullable=False)

    ## criar o vinculo com o modelo do veiculo
    modelo = relationship("Marca", back_populates="veiculos")
     
    def __init__(self, placa: str, codigo_modelo: Integer):
        """
        Cria uma modelo de veiculo de marca especifica

        Argumentos:
            des_placa: placa
            cod_modelo: codigo_modelo
        """
        self.des_placa = placa
        self.cod_modelo = codigo_modelo
