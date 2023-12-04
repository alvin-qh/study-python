import pytest

from basic import app
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client() -> TestClient:
    client = TestClient(app)
    return client


def test_basic_api(client: TestClient) -> None:
    response = client.get("/api/hello")
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "payload": {
            "message": "Hello World",
        },
    }
