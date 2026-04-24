import pytest
import app.routes as routes_module
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    # resetea la lista antes de cada test
    routes_module.users = [
        {"id": 1, "nombre": "Juan", "apellido": "Perez", "rol": "admin"},
        {"id": 2, "nombre": "Ana", "apellido": "Garcia", "rol": "user"},
    ]
    with app.test_client() as client:
        yield client

# Health
def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"

# GET /users
def test_get_users_retorna_lista(client):
    res = client.get("/users")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

def test_get_users_tiene_dos_usuarios(client):
    res = client.get("/users")
    assert len(res.get_json()) == 2

# GET /users/<id>
def test_get_user_existente(client):
    res = client.get("/users/1")
    assert res.status_code == 200
    assert res.get_json()["nombre"] == "Juan"

def test_get_user_no_existente(client):
    res = client.get("/users/9999")
    assert res.status_code == 404

# POST /users
def test_create_user(client):
    res = client.post("/users", json={
        "nombre": "Carlos",
        "apellido": "Lopez",
        "rol": "user"
    })
    assert res.status_code == 201
    assert res.get_json()["nombre"] == "Carlos"

def test_create_user_genera_id(client):
    res = client.post("/users", json={
        "nombre": "Carlos",
        "apellido": "Lopez",
        "rol": "user"
    })
    assert res.get_json()["id"] == 3

def test_create_user_faltan_campos(client):
    res = client.post("/users", json={"nombre": "Solo nombre"})
    assert res.status_code == 400

# PUT /users/<id>
def test_update_user(client):
    res = client.put("/users/1", json={
        "nombre": "Juan",
        "apellido": "Perez",
        "rol": "superadmin"
    })
    assert res.status_code == 200
    assert res.get_json()["rol"] == "superadmin"

def test_update_user_no_existente(client):
    res = client.put("/users/9999", json={
        "nombre": "X",
        "apellido": "Y",
        "rol": "user"
    })
    assert res.status_code == 404

# DELETE /users/<id>
def test_delete_user(client):
    res = client.delete("/users/1")
    assert res.status_code == 200

def test_delete_user_no_existente(client):
    res = client.delete("/users/9999")
    assert res.status_code == 404

def test_delete_user_reduce_lista(client):
    client.delete("/users/1")
    res = client.get("/users")
    assert len(res.get_json()) == 1