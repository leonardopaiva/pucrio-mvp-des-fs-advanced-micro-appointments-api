from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from model.event import Event, EventType
from enum import Enum

from schemas import ComentarioSchema


class EventSchema(BaseModel):
    """
    Define como um novo event a ser inserido deve ser representado.
    O campo "id" é opcional, pois pode ser gerado automaticamente (ex.: UUID)
    """
    id: Optional[str] = None
    name: str = "Consulta Dermatologista"
    description: str = "A consulta será por ordem de chegada"
    observation: str = "Vou precisar de ajuda para ir até a consulta porque o carro está quebrado"
    date: datetime = datetime.now()
    doctor_name: str = "Doutor Matheus"
    location_name: str = "memorial são jose recife 83"
    location_id: int = 1
    doctor_id: int = 1
    user_id: str = "default_user_id"
    type: EventType = EventType.CONSULTATION


class EventBuscaSchema(BaseModel):
    """
    Define como deve ser a estrutura que representa a busca,
    utilizando os campos "id" e "user_id".
    """
    id: str = "1"
    user_id: str = "54e8a4a8-5001-7018-8eec-ce6b634cded9"


class ListagemEventsSchema(BaseModel):
    """
    Define como uma listagem de events será retornada.
    """
    events: List[EventSchema]


def apresenta_events(events: List[Event]):
    """
    Retorna uma representação dos events seguindo o schema definido,
    incluindo o campo "id" de cada evento.
    """
    result = []
    for event in events:
        result.append({
            "id": event.id,
            "name": event.name,
            "description": event.description,
            "observation": event.observation,
            "date": event.date,
            "doctor_name": event.doctor_name,
            "location_name": event.location_name,
            "location_id": event.location_id,
            "doctor_id": event.doctor_id,
            "user_id": event.user_id,
            "type": event.type,
        })
    return {"events": result}


class EventViewSchema(BaseModel):
    """
    Define como um event será retornado, incluindo comentários.
    """
    id: str = "1"
    name: str = "Consulta Dermatologista"
    description: str = "A consulta será por ordem de chegada"
    observation: str = "Vou precisar de ajuda para ir até a consulta porque o carro está quebrado"
    date: datetime = datetime.now()
    doctor_name: str = "Doutor Matheus"
    location_name: str = "memorial são jose recife 83"
    location_id: int = 1
    doctor_id: int = 1
    user_id: str = "default_user_id"
    type: EventType = EventType.CONSULTATION
    total_cometarios: int = 1
    comentarios: List[ComentarioSchema]


class EventDelSchema(BaseModel):
    """
    Define como deve ser a estrutura do dado retornado após uma requisição de remoção.
    """
    mesage: str
    name: str


def apresenta_event(event: Event):
    """
    Retorna uma representação detalhada do event, seguindo o schema EventViewSchema.
    """
    return {
        "id": event.id,
        "name": event.name,
        "description": event.description,
        "observation": event.observation,
        "date": event.date,
        "doctor_name": event.doctor_name,
        "location_name": event.location_name,
        "location_id": event.location_id,
        "doctor_id": event.doctor_id,
        "user_id": event.user_id,
        "type": event.type,
        "total_cometarios": len(event.comentarios),
        "comentarios": [{"texto": c.texto} for c in event.comentarios]
    }
