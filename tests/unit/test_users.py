import pytest
from app import create_app
from app.db import get_connection

@pytest.fixture(autouse=True)
def clean_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users")
    cur.execute("INSERT INTO users (nombre, apellido, rol) VALUES ('Juan', 'Perez', 'admin')")
    cur.execute("INSERT INTO users (nombre, apellido, rol) VALUES ('Ana', 'Garcia', 'user')")
    conn.commit()
    cur.close()
    conn.close()

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"

def test_get_users_retorna_lista(client):
    res = client.get("/users")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

def test_get_users_tiene_dos_usuarios(client):
    res = client.get("/users")
    assert len(res.get_json()) == 2

def test_get_user_existente(client):
    res = client.get("/users")
    user_id = res.get_json()[0]["id"]
    res = client.get(f"/users/{user_id}")
    assert res.status_code == 200
    assert res.get_json()["nombre"] == "Juan"

def test_get_user_no_existente(client):
    res = client.get("/users/9999")
    assert res.status_code == 404

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
    assert "id" in res.get_json()

def test_create_user_faltan_campos(client):
    res = client.post("/users", json={"nombre": "Solo nombre"})
    assert res.status_code == 400

def test_update_user(client):
    res = client.get("/users")
    user_id = res.get_json()[0]["id"]
    res = client.put(f"/users/{user_id}", json={
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

def test_delete_user(client):
    res = client.get("/users")
    user_id = res.get_json()[0]["id"]
    res = client.delete(f"/users/{user_id}")
    assert res.status_code == 200

def test_delete_user_no_existente(client):
    res = client.delete("/users/9999")
    assert res.status_code == 404

def test_delete_user_reduce_lista(client):
    res = client.get("/users")
    user_id = res.get_json()[0]["id"]
    client.delete(f"/users/{user_id}")
    res = client.get("/users")
    assert len(res.get_json()) == 1