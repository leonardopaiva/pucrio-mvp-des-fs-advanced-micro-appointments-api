from sqlalchemy.exc import IntegrityError
from urllib.parse import unquote
import uuid
import pudb
from datetime import datetime
from model import Session, Event, Comentario
from schemas.event import (
    EventSchema,
    EventBuscaSchema,
    EventViewSchema,
    ListagemEventsSchema,
    EventDelSchema,
    apresenta_events,
    apresenta_event
)
from logger import logger
from flask import request

#EventService
# Responsible for communicating with the appointments database, GET, POST, PUT and DELETE, all operations use
# the user id and the appointment id, preventing one user from modifying another's item.
class EventService:
    #POST
    def add_event(body: EventSchema):
        event_id = str(uuid.uuid4())
        event = Event(
            id=event_id,
            name=body.name,
            date=body.date,
            type=body.type,
            description=body.description,
            observation=body.observation,
            doctor_name=body.doctor_name,
            location_name=body.location_name,
            location_id=body.location_id,
            doctor_id=body.doctor_id,
            user_id=body.user_id
        )
        logger.debug(f"Adicionando event de name: '{event.name}' com id: '{event.id}'")
        try:
            session = Session()
            session.add(event)
            session.commit()
            logger.debug(f"Adicionado event de name: '{event.name}' com id: '{event.id}'")
            return {"status": "ok", "msg": "Event adicionado com sucesso.", "data": apresenta_event(event)}, 200
        except IntegrityError as e:
            error_msg = f"Erro de integridade ao adicionar event: {e.orig if hasattr(e, 'orig') else str(e)}"
            logger.warning(f"Erro ao adicionar event '{event.name}': {error_msg}")
            return {"status": "error", "msg": error_msg, "data": {}}, 409
        except Exception as e:
            error_msg = "Não foi possível salvar novo item :/"
            logger.info("****************** ERROR ****************************")
            logger.warning(e)
            logger.info("*************************************************************")
            logger.warning(f"Erro ao adicionar event '{event.name}': {error_msg} - {e}")
            return {"status": "error", "msg": error_msg, "data": {}}, 400

    #GET
    def get_events():
        logger.debug("Coletando events")
        session = Session()
        user_id = request.args.get("user_id")
        if user_id:
            events = session.query(Event).filter(Event.user_id == user_id).all()
            logger.debug(f"{len(events)} events encontrados para user_id {user_id}")
        else:
            events = session.query(Event).all()
            logger.debug(f"{len(events)} events encontrados (sem filtro)")
        if not events:
            return {"status": "ok", "msg": "Nenhum event encontrado.", "data": []}, 200
        else:
            logger.debug(f"Retornando {len(events)} events")
            teste = apresenta_events(events)
            print(teste)
            return {"status": "ok", "msg": "Events coletados com sucesso.", "data": apresenta_events(events)}, 200
    #GET
    def get_event(query: EventBuscaSchema):
        event_id = query.id
        logger.debug(f"Coletando dados sobre event #{event_id}")
        session = Session()
        event = session.query(Event).filter(Event.name == event_id).first()
        if not event:
            error_msg = "Event não encontrado na base :/"
            logger.warning(f"Erro ao buscar event '{event_id}': {error_msg}")
            return {"status": "error", "msg": error_msg, "data": {}}, 404
        else:
            logger.debug(f"Event encontrado: '{event.id}'")
            return {"status": "ok", "msg": "Event encontrado.", "data": apresenta_event(event)}, 200

    #DELETE
    def del_event_by_id_and_user(query: EventBuscaSchema):
        """
        Deleta um event específico utilizando os campos 'id' e 'user_id' informados no query.
        Retorna no campo "data" os dados do event que foi deletado.
        """
        try:
            event_id = query.id
        except Exception as e:
            return {"status": "error", "msg": f"Invalid id format: {str(e)}", "data": {}}, 400

        user_id = query.user_id
        if not user_id:
            return {"status": "error", "msg": "Missing user_id in query", "data": {}}, 400

        session = Session()
        event = session.query(Event).filter(Event.id == event_id, Event.user_id == user_id).first()
        if not event:
            return {"status": "error", "msg": "Event não encontrado ou não pertence ao usuário", "data": {}}, 404

        event_data = apresenta_event(event)
        count = session.query(Event).filter(Event.id == event_id, Event.user_id == user_id).delete()
        session.commit()
        if count:
            return {"status": "ok", "msg": "Event removido", "data": event_data}, 200
        else:
            return {"status": "error", "msg": "Event não encontrado ou não pertence ao usuário", "data": {}}, 404

    #PUT
    def update_event(query: EventBuscaSchema, body: EventSchema):
        """
        Atualiza um event existente utilizando os campos 'id' e 'user_id' informados no query,
        e os dados enviados no body.
        Retorna uma representação do event atualizado.
        """
        event_id = query.id
        user_id = query.user_id
        session = Session()
        event = session.query(Event).filter(Event.id == event_id, Event.user_id == user_id).first()
        if not event:
            error_msg = "Event não encontrado ou não pertence ao usuário"
            logger.warning(f"Erro ao atualizar event '{event_id}': {error_msg}")
            return {"status": "error", "msg": error_msg, "data": {}}, 404
        try:
            payload = body.dict(exclude_unset=True)
            for key, value in payload.items():
                if key == "type" and hasattr(value, "value"):
                    value = value.value
                setattr(event, key, value)
            event.updated_at = datetime.now()
            session.commit()
            logger.debug(f"Event atualizado: '{event.id}'")
            return {"status": "ok", "msg": "Event atualizado com sucesso.", "data": apresenta_event(event)}, 200
        except IntegrityError as e:
            session.rollback()
            detail = e.orig if hasattr(e, 'orig') else str(e)
            error_msg = f"Erro de integridade ao atualizar event: {detail}"
            logger.warning(f"Erro ao atualizar event '{event.id}': {error_msg}")
            return {"status": "error", "msg": error_msg, "data": {}}, 409
        except Exception as e:
            session.rollback()
            error_msg = f"Não foi possível atualizar o event: {str(e)}"
            logger.warning(f"Erro ao atualizar event '{event.id}': {error_msg}")
            return {"status": "error", "msg": error_msg, "data": {}}, 400

    #OTHER
    #used to save comments on appointments items, but not used right now.
    def add_comentario(form):
        try:
            event_id = form.event_id
            if not event_id:
                error_msg = "Event id inválido :/"
                logger.warning(f"Operação inválida '{event_id}': {error_msg}")
                return {"status": "error", "msg": error_msg, "data": {}}, 404
            logger.debug(f"Adicionando comentários ao event #{event_id}")
            session = Session()
            event = session.query(Event).filter(Event.id == event_id).first()
            if not event:
                error_msg = "Event não encontrado na base :/"
                logger.warning(f"Erro ao adicionar comentário ao event '{event_id}': {error_msg}")
                return {"status": "error", "msg": error_msg, "data": {}}, 404
            texto = form.texto
            comentario = Comentario(texto)
            event.adiciona_comentario(comentario)
            session.commit()
            logger.debug(f"Adicionado comentário ao event #{event_id}")
            return {"status": "ok", "msg": "Comentário adicionado com sucesso.", "data": apresenta_event(event)}, 200
        except IntegrityError as e:
            error_msg = f"Erro ao adicionar comentário, duplicidade detectada: {e.orig if hasattr(e, 'orig') else str(e)}"
            logger.warning(f"Erro ao adicionar comentário: {error_msg}")
            return {"status": "error", "msg": error_msg, "data": {}}, 409
        except Exception as e:
            error_msg = f"Não foi possível salvar novo item: {str(e)}"
            logger.info("****************** ERROR ****************************")
            logger.warning(e)
            logger.info("*************************************************************")
            logger.warning(f"Erro ao adicionar comentário: {error_msg}")
            return {"status": "error", "msg": error_msg, "data": {}}, 400
