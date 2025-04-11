import sys
import os
# Add the project's root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import app as app_module  # Import the app module for patching functions
from app import app      # Import the Flask app instance

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_add_appointment_success(client, monkeypatch):
    # Simulate a successful appointment creation
    def fake_add_event(body):
        # Converte o objeto Pydantic para dict para acessar seus valores
        b = body.dict()
        # Converte o campo 'type' para o valor primitivo, se necessário
        type_val = b.get("type", 1)
        if hasattr(type_val, "value"):
            type_val = type_val.value
        # Monta a resposta fake com os dados
        event = {
            "id": "1",
            "name": b.get("name", "Consulta Dermatologista"),
            "description": b.get("description", "A consulta será por ordem de chegada"),
            "observation": b.get("observation", "Vou precisar de ajuda para ir até a consulta porque o carro está quebrado"),
            "date": b.get("date"),
            "doctor_name": b.get("doctor_name", "Doutor Matheus"),
            "location_name": b.get("location_name", "memorial são jose recife 83"),
            "location_id": b.get("location_id", 1),
            "doctor_id": b.get("doctor_id", 1),
            "user_id": b.get("user_id", "default_user_id"),
            "type": type_val,
            "total_cometarios": 0,
            "comentarios": []
        }
        return {"status": "ok", "msg": "Event adicionado com sucesso.", "data": event}, 200

    # Patch usando a função add_event do EventService
    monkeypatch.setattr(app_module.EventService, "add_event", fake_add_event)

    payload = {
        "name": "Consulta Dermatologista",
        "description": "Consulta para avaliação de pele",
        "observation": "Exemplo de observação",
        "date": "2023-04-01T10:00:00",
        "doctor_name": "Doutor Matheus",
        "location_name": "memorial são jose recife 83",
        "location_id": 1,
        "doctor_id": 1,
        "user_id": "default_user_id",
        "type": 1
    }
    response = client.post("/appointment", json=payload)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    result = response.get_json()
    assert result["status"] == "ok", "Expected status 'ok'"
    assert "id" in result["data"], "Expected event id in response data"

def test_add_appointment_missing_field(client, monkeypatch):
    # Patch a versão fake da função add_event para simular erro quando "name" estiver ausente ou vazio
    def fake_add_event(body):
        b = body.dict()
        # Se "name" não estiver presente ou estiver vazio, simula erro de duplicidade
        if "name" not in b or not b.get("name"):
            return {"status": "error", "msg": "Erro de integridade: UNIQUE constraint failed: event.name", "data": {}}, 409
        # Converte o campo 'type'
        type_val = b.get("type", 1)
        if hasattr(type_val, "value"):
            type_val = type_val.value
        event = {
            "id": "1",
            "name": b.get("name", "Consulta Dermatologista"),
            "description": b.get("description", "A consulta será por ordem de chegada"),
            "observation": b.get("observation", "Vou precisar de ajuda para ir até a consulta porque o carro está quebrado"),
            "date": b.get("date"),
            "doctor_name": b.get("doctor_name", "Doutor Matheus"),
            "location_name": b.get("location_name", "memorial são jose recife 83"),
            "location_id": b.get("location_id", 1),
            "doctor_id": b.get("doctor_id", 1),
            "user_id": b.get("user_id", "default_user_id"),
            "type": type_val,
            "total_cometarios": 0,
            "comentarios": []
        }
        return {"status": "ok", "msg": "Event adicionado com sucesso.", "data": event}, 200

    monkeypatch.setattr(app_module.EventService, "add_event", fake_add_event)

    payload = {
        # Força o campo "name" a ser vazio para simular ausência
        "name": "",
        "description": "Consulta para avaliação de pele",
        "observation": "Exemplo de observação",
        "date": "2023-04-01T10:00:00",
        "doctor_name": "Doutor Matheus",
        "location_name": "memorial são jose recife 83",
        "location_id": 1,
        "doctor_id": 1,
        "user_id": "default_user_id",
        "type": 1
    }
    response = client.post("/appointment", json=payload)
    # Espera retornar 409 (erro de duplicidade)
    assert response.status_code == 409, f"Expected 409 for missing field, got {response.status_code}"

def test_get_appointments(client, monkeypatch):
    # Simulate retrieving a list of appointments
    def fake_get_events():
        events = [
            {
                "id": "1",
                "name": "Consulta Dermatologista",
                "description": "Consulta para avaliação de pele",
                "observation": "Exemplo de observação",
                "date": "2023-04-01T10:00:00",
                "doctor_name": "Doutor Matheus",
                "location_name": "memorial são jose recife 83",
                "location_id": 1,
                "doctor_id": 1,
                "user_id": "default_user_id",
                "type": 1,
                "total_cometarios": 0,
                "comentarios": []
            }
        ]
        return {"status": "ok", "msg": "Events coletados com sucesso.", "data": {"events": events}}, 200

    monkeypatch.setattr(app_module, "get_events", fake_get_events)

    response = client.get("/appointments")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    result = response.get_json()
    assert "events" in result["data"], "Expected 'events' key in response data"
    assert isinstance(result["data"]["events"], list), "Expected events to be a list"

def test_delete_appointment_success(client, monkeypatch):
    # Simulate successful deletion of an appointment
    def fake_del_event(query):
        return {"status": "ok", "msg": "Event removido", "data": {"id": query.id, "name": "Consulta Dermatologista"}}, 200

    monkeypatch.setattr(app_module.EventService, "del_event_by_id_and_user", fake_del_event)
    response = client.delete("/appointment?id=1&user_id=default_user_id")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    result = response.get_json()
    assert result["status"] == "ok", "Expected status 'ok' after deletion"
    assert "Event removido" in result["msg"], "Expected deletion confirmation message"

def test_update_appointment_success(client, monkeypatch):
    # Simulate a successful update of an appointment
    def fake_update_event(query, body):
        # Converte o campo 'type' para um valor serializável, se necessário
        type_val = body.type
        if hasattr(type_val, "value"):
            type_val = type_val.value
        updated_event = {
            "id": query.id,
            "name": body.name,
            "description": body.description,
            "observation": body.observation,
            "date": body.date,
            "doctor_name": body.doctor_name,
            "location_name": body.location_name,
            "location_id": body.location_id,
            "doctor_id": body.doctor_id,
            "user_id": body.user_id,
            "type": type_val,
            "total_cometarios": 0,
            "comentarios": []
        }
        return {"status": "ok", "msg": "Event atualizado com sucesso.", "data": updated_event}, 200

    monkeypatch.setattr(app_module.EventService, "update_event", fake_update_event)
    payload = {
        "name": "Consulta Alterada",
        "description": "Consulta atualizada",
        "observation": "Observação atualizada",
        "date": "2023-04-02T10:00:00",
        "doctor_name": "Doutor Matheus",
        "location_name": "memorial são jose recife 83",
        "location_id": 1,
        "doctor_id": 1,
        "user_id": "default_user_id",
        "type": 1
    }
    response = client.put("/appointment?id=1&user_id=default_user_id", json=payload)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    result = response.get_json()
    assert result["status"] == "ok", "Expected status 'ok' after update"
    updated = result["data"]
    assert updated["name"] == "Consulta Alterada", "Expected updated name in response"
