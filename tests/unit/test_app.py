import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    res = client.get("/")
    assert res.status_code == 200
