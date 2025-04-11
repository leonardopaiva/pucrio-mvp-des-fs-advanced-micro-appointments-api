from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Doctor(Base):
    __tablename__ = 'doctor'

    id = Column("pk_doctor", Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)
    observation = Column(String(255), nullable=True)
    data_insercao = Column(DateTime, default=datetime.now)

    # definindo relactionamentos, em um futuro, estudar como definir
    # caso o doutor tenha mais de uma localização e mais de uma especialidade
    # além disso estudar como retornar o objeto com os dados do banco de dados, 
    # tanto para location_id, quando para specialty_id e não apenas, retornar o ID
    location_id = Column(Integer, ForeignKey("location.pk_location"), nullable=True)

    # Definição do relacionamento entre o doctor e o comentário.
    # Essa relação é implicita, não está salva na tabela 'doctor',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, 
                 name:str,
                 email: str,
                 phone: str,
                 observation: str,
                 location_id: int,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Doctor

        Arguments:
            name: name do doctor.
            data_insercao: data de quando o doctor foi inserido à base
        """
        self.name = name
        self.email = email
        self.phone = phone
        self.observation = observation
        self.location_id = location_id

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao Doctor
        """
        self.comentarios.append(comentario)

