from typing import cast

import pytest
from bs4 import BeautifulSoup
from error_handler import app
from tests import nn

from flask.testing import FlaskClient


@pytest.fixture(scope="module")
def client() -> FlaskClient:
    """定义获取 Flask 测试客户端的 fixture"""
    return cast(FlaskClient, app.test_client())


def test_get_index(client: FlaskClient) -> None:
    resp = client.get("/")
    assert resp.status_code == 200

    soup = BeautifulSoup(resp.data, "html.parser")
    assert [a["href"] for a in soup.select("nav a")] == [
        "/not-exist-url",
        "/exception",
    ]


def test_get_not_exist_error(client: FlaskClient) -> None:
    resp = client.get("/not-exist-url")
    assert resp.status_code == 404

    soup = BeautifulSoup(resp.data, "html.parser")
    assert nn(soup.select_one(".error h2")).string == "Page was gone with wind"
    assert nn(soup.select_one(".error p")).string == (
        "404 Not Found: The requested URL was not found on the server. "
        "If you entered the URL manually please check your spelling and try again."
    )


def test_get_exception(client: FlaskClient) -> None:
    resp = client.get("/exception")
    assert resp.status_code == 500

    soup = BeautifulSoup(resp.data, "html.parser")
    assert nn(soup.select_one(".error h2")).string == "Exception was caused"
    assert nn(soup.select_one(".error p")).string == "Oh shit!!"

    trace = nn(soup.select_one(".error pre")).string
    assert (
        'study-python/web/flask/src/error_handler/app.py"'
        in trace
    )
    assert 'raise NothingError("Oh shit!!")' in trace
