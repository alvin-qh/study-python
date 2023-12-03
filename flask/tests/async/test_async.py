from typing import Any, Dict, cast

import pytest
from async_ import app

from flask.testing import FlaskClient


@pytest.fixture(scope="module")
def client() -> FlaskClient:
    """定义获取 Flask 测试客户端的 fixture"""
    return cast(FlaskClient, app.test_client())


def test_get_index(client: FlaskClient) -> None:
    """测试 GET / 路由调用"""

    resp = client.get("/")

    assert resp.status_code == 200
    assert b'<script src="/static/script/show-time.js"></script>' in resp.data


def test_get_json(client: FlaskClient) -> None:
    """测试 GET /json 路由调用"""

    resp = client.get("/json")

    assert resp.status_code == 200

    json_data: Dict[str, Any] = cast(Dict[str, Any], resp.json)
    assert "time" in json_data
    assert isinstance(json_data["time"], int)
