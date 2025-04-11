from pydantic import BaseModel
from typing import Optional, List
from model.doctor import Doctor

from schemas import ComentarioSchema


class DoctorSchema(BaseModel):
    """ Define como um novo doctor a ser inserido deve ser representado
    """
    name: str = "Doutor Matias"
    observation: str = ""
    email: str = ""
    phone: str = ""
    location_id: int = 1



class DoctorBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no name do doctor.
    """
    name: str = "Doutor Matias"


class ListagemDoctorsSchema(BaseModel):
    """ Define como uma listagem de doctors será retornada.
    """
    doctors:List[DoctorSchema]


def apresenta_doctors(doctors: List[Doctor]):
    """ Retorna uma representação do doctor seguindo o schema definido em
        DoctorViewSchema.
    """
    result = []
    for doctor in doctors:
        result.append({
            "name": doctor.name,
            "email": doctor.email,
            "phone": doctor.phone,
            "observation": doctor.observation,
            "location_id": doctor.location_id,
        })

    return {"doctors": result}


class DoctorViewSchema(BaseModel):
    """ Define como um doctor será retornado: doctor + comentários.
    """
    id: int = 1
    name: str = "Doutor Matias"
    email: str = ""
    phone: str = ""
    observation: str = ""
    location_id: int = 1
    total_cometarios: int = 1
    comentarios:List[ComentarioSchema]


class DoctorDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    name: str

def apresenta_doctor(doctor: Doctor):
    """ Retorna uma representação do doctor seguindo o schema definido em
        DoctorViewSchema.
    """
    return {
        "id": doctor.id,
        "name": doctor.name,
        "email": doctor.email,
        "phone": doctor.phone,
        "observation": doctor.observation,
        "location_id": doctor.location_id,
        "total_cometarios": len(doctor.comentarios),
        "comentarios": [{"texto": c.texto} for c in doctor.comentarios]
    }
