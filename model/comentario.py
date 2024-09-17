from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Comentario(Base):
    __tablename__ = 'comentario'

    id = Column(Integer, primary_key=True)
    texto = Column(String(4000))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o comentário e um produto.
    # Aqui está sendo definido a coluna 'produto' que vai guardar
    # a referencia ao produto, a chave estrangeira que relaciona
    # um produto ao comentário.
    produto = Column(Integer, ForeignKey("produto.pk_produto"), nullable=True)

    # Definição do relacionamento entre o comentário e um event.
    # Aqui está sendo definido a coluna 'event' que vai guardar
    # a referencia ao event, a chave estrangeira que relaciona
    # um event ao comentário.
    event = Column(Integer, ForeignKey("event.pk_event"), nullable=True)
    doctor = Column(Integer, ForeignKey("doctor.pk_doctor"), nullable=True)
    specialty = Column(Integer, ForeignKey("specialty.pk_specialty"), nullable=True)
    location = Column(Integer, ForeignKey("location.pk_location"), nullable=True)

    def __init__(self, texto:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria um Comentário

        Arguments:
            texto: o texto de um comentário.
            data_insercao: data de quando o comentário foi feito ou inserido
                           à base
        """
        self.texto = texto
        if data_insercao:
            self.data_insercao = data_insercao
