from urllib.parse import quote

from fastapi.testclient import TestClient


def test_hello_api_with_query_args(client: TestClient) -> None:
    response = client.get(f"/api/hello?name={quote('Alvin')}&gender=M")
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "payload": {
            "message": "Hello Mr. Alvin",
        },
    }


def test_hello_api_without_query_args(client: TestClient) -> None:
    response = client.get("/api/hello")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": None,
                "loc": ["query", "name"],
                "msg": "Field required",
                "type": "missing",
            }
        ],
    }


def test_hello_api_without_name_query_arg(client: TestClient) -> None:
    response = client.get(f"/api/hello?name={quote('  ')}")
    assert response.status_code == 400
    assert response.json() == {
        "status": "error",
        "payload": {
            "message": "Name is required",
        },
    }


def test_basic_api_with_path_param(client: TestClient) -> None:
    response = client.get(f"/api/hello/{quote('Emma')}?gender=F")
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "payload": {
            "message": "Hello Ms. Emma",
        },
    }


def test_basic_api_with_wrong_path_param(client: TestClient) -> None:
    response = client.get(f"/api/hello/{quote('  ')}")
    assert response.status_code == 400
    assert response.json() == {
        "status": "error",
        "payload": {
            "message": "Name is required",
        },
    }
