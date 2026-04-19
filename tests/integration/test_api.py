import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_response_is_html(client):
    res = client.get("/")
    assert b"Hello" in res.data
