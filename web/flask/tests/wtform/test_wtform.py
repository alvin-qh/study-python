from typing import cast

import pytest
from wtform import app

from flask.testing import FlaskClient


@pytest.fixture(scope="module")
def client() -> FlaskClient:
    """定义获取 Flask 测试客户端的 fixture"""
    return cast(FlaskClient, app.test_client())


def test_index_get(client: FlaskClient) -> None:
    resp = client.get("/")

    assert resp.status_code == 200


def test_index_post_and_400_caused(client: FlaskClient) -> None:
    resp = client.post("/")

    assert resp.status_code == 400

    assert b'<div class="error">Number a required</div>' in resp.data
    assert b'<div class="error">Number b required</div>' in resp.data
    assert (
        b'<div class="error">Operator must on of &#34;+. -, *, /&#34;</div>'
        in resp.data
    )


def test_index_post(client: FlaskClient) -> None:
    resp = client.post("/", data={"a": 1, "b": 2, "op": "+"})

    assert resp.status_code == 200
    assert b'<div class="field"><input value="3.0" /></div>' in resp.data


def test_ajax_post_and_400_caused(client: FlaskClient) -> None:
    resp = client.post("/ajax", json={})
    assert resp.status_code == 400

    assert resp.json == {
        "errors": {
            "a": ["Number a required"],
            "b": ["Number b required"],
            "op": ['Operator must on of "+. -, *, /"'],
        }
    }


def test_ajax_post(client: FlaskClient) -> None:
    resp = client.post("/ajax", json={"a": 1, "b": 2, "op": "+"})

    assert resp.status_code == 200

    assert resp.json == {"ans": 3.0}
