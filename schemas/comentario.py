from typing import Optional
from pydantic import BaseModel


class ComentarioSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado
    """
    user_id: Optional[int] = None
    doctor_id: Optional[int] = None
    location_id: Optional[int] = None
    event_id: Optional[int] = None
    texto: str = "Só comprar se o preço realmente estiver bom!"
