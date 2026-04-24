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

def test_method_not_allowed_health(client):
    res = client.post("/health")
    assert res.status_code == 405

def test_create_user_empty_body(client):
    res = client.post("/users", json={})
    assert res.status_code == 400

def test_create_user_invalid_content_type(client):
    res = client.post("/users", data="not json", content_type="text/plain")
    assert res.status_code in (400, 415)

def test_delete_nonexistent_user(client):
    res = client.delete("/users/9999")
    assert res.status_code == 404

def test_put_nonexistent_user(client):
    res = client.put("/users/9999", json={
        "nombre": "X",
        "apellido": "Y",
        "rol": "user"
    })
    assert res.status_code == 404