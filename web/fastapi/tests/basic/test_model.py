from datetime import date

from fastapi.testclient import TestClient

from basic.model import Gender, User


def test_create_and_query_model(client: TestClient) -> None:
    user = User(
        name="Alvin",
        gender=Gender.MALE,
        email="alvin@fakemail.com",
        birthday=date(1981, 3, 17),
    )

    response = client.post("/api/user", json=user.model_dump())
    assert response.status_code == 200

    result = response.json()
    assert result["payload"]["user"]["id"] is not None

    id = result["payload"]["user"]["id"]
    del result["payload"]["user"]["id"]

    assert result == {
        "status": "success",
        "payload": {
            "user": {
                "name": "Alvin",
                "gender": "male",
                "birthday": "1981-03-17",
                "email": "alvin@fakemail.com",
            },
        },
    }

    response = client.get(f"/api/user/{id}")
    assert response.status_code == 200

    result = response.json()
    assert result["payload"]["user"]["id"] == id

    del result["payload"]["user"]["id"]

    assert result == {
        "status": "success",
        "payload": {
            "user": {
                "name": "Alvin",
                "gender": "male",
                "birthday": "1981-03-17",
                "email": "alvin@fakemail.com",
            },
        },
    }
