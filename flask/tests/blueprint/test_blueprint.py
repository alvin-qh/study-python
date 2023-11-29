from typing import cast
from urllib.parse import quote

import pytest
from blueprint import app
from bs4 import BeautifulSoup
from tests import nn

from flask.testing import FlaskClient


@pytest.fixture(scope="module")
def client() -> FlaskClient:
    """定义获取 Flask 测试客户端的 fixture"""
    return cast(FlaskClient, app.test_client())


def test_home(client: FlaskClient) -> None:
    resp = client.get("/")
    assert resp.status_code == 200

    soup = BeautifulSoup(resp.data, "html.parser")
    assert nn(nn(soup.title).string).strip() == "Blueprint Demo"
    assert [link["href"] for link in soup.select("head>link[rel=stylesheet]")] == [
        "/static/css/common.css?__v=598a260083014b47"
    ]
    assert [script["src"] for script in soup.select("body>script")] == [
        "/static/script/home.js?__v=d2d7711f3a42ae0d"
    ]
    assert nn(soup.select_one("main .text-right a"))["href"] == "/user"


def test_user_success(client: FlaskClient) -> None:
    resp = client.get(f"/user?name={quote('Alvin')}")
    assert resp.status_code == 200

    soup = BeautifulSoup(resp.data, "html.parser")
    assert nn(soup.select_one("header h2.text-center")).string == "Hello Alvin"


def test_user_error(client: FlaskClient) -> None:
    resp = client.get("/user")
    assert resp.status_code == 200

    soup = BeautifulSoup(resp.data, "html.parser")

    result = nn(soup.select_one("header h2.text-center"))
    assert "text-danger" in result["class"]
    assert result.string == "Invalid user name"
