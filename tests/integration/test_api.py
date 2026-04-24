import pytest
from app import app
from app.db import get_connection

@pytest.fixture(autouse=True)
def clean_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users")
    conn.commit()
    cur.close()
    conn.close()

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_user_lifecycle(client):
    res = client.post("/users", json={
        "nombre": "Maria",
        "apellido": "Gomez",
        "rol": "admin"
    })
    assert res.status_code == 201
    user_id = res.get_json()["id"]

    res = client.get(f"/users/{user_id}")
    assert res.status_code == 200
    assert res.get_json()["apellido"] == "Gomez"

    res = client.put(f"/users/{user_id}", json={
        "nombre": "Maria",
        "apellido": "Gomez",
        "rol": "superadmin"
    })
    assert res.status_code == 200
    assert res.get_json()["rol"] == "superadmin"

    res = client.delete(f"/users/{user_id}")
    assert res.status_code == 200

    res = client.get(f"/users/{user_id}")
    assert res.status_code == 404