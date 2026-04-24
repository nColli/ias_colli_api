import pytest
import app.routes as routes_module
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    routes_module.users = [
        {"id": 1, "nombre": "Juan", "apellido": "Perez", "rol": "admin"},
        {"id": 2, "nombre": "Ana", "apellido": "Garcia", "rol": "user"},
    ]
    with app.test_client() as client:
        yield client

def test_user_lifecycle(client):
    # Crear
    res = client.post("/users", json={
        "nombre": "Maria",
        "apellido": "Gomez",
        "rol": "admin"
    })
    assert res.status_code == 201
    user_id = res.get_json()["id"]

    # Obtener
    res = client.get(f"/users/{user_id}")
    assert res.status_code == 200
    assert res.get_json()["apellido"] == "Gomez"

    # Actualizar
    res = client.put(f"/users/{user_id}", json={
        "nombre": "Maria",
        "apellido": "Gomez",
        "rol": "superadmin"
    })
    assert res.status_code == 200
    assert res.get_json()["rol"] == "superadmin"

    # Eliminar
    res = client.delete(f"/users/{user_id}")
    assert res.status_code == 200

    # Verificar que no existe más
    res = client.get(f"/users/{user_id}")
    assert res.status_code == 404