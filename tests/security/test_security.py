import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_method_not_allowed(client):
    res = client.post("/")
    assert res.status_code == 405
