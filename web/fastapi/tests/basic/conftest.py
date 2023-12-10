from fastapi.testclient import TestClient
from pytest import fixture


@fixture(scope="package", autouse=True)
def client() -> TestClient:
    from basic import app

    return TestClient(app)
