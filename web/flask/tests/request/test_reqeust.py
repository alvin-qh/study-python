from typing import cast
from flask.testing import FlaskClient
import pytest
from request import app, get_names, clear_names
from urllib.parse import quote


@pytest.fixture(scope="module")
def client() -> FlaskClient:
    """定义获取 Flask 测试客户端的 fixture"""
    return cast(FlaskClient, app.test_client())


def setup_function() -> None:
    """每次测试前运行一次"""
    clear_names()


def test_post_index(client: FlaskClient) -> None:
    """测试 POST 请求, 添加一个名词内容"""

    resp = client.post(
        "/",
        data={  # 通过 data 发送 form 数据
            "name": "Alvin",
        },
    )
    assert resp.status_code == 302
    assert resp.headers.get("Location") == "/"

    assert get_names() == ["Alvin"]


def test_put_index(client: FlaskClient) -> None:
    """测试 POST 请求, 修改一个名词内容"""

    resp = client.post(
        "/",
        data={  # 通过 data 发送 form 数据
            "name": "Alvin",
        },
    )
    assert resp.status_code == 302
    assert resp.headers.get("Location") == "/"

    # 发送 PUT 请求
    resp = client.put(
        "/",
        data={
            "new_value": "Emma",
        },
    )

    assert resp.status_code == 302
    assert resp.headers.get("Location") == "/"

    assert set(get_names()) == set(["Alvin", "Emma"])

    # 发送 PUT 请求
    resp = client.put(
        "/",
        data={
            "old_value": "Alvin",
            "new_value": "Tom",
        },
    )

    assert resp.status_code == 302
    assert resp.headers.get("Location") == "/"

    assert set(get_names()) == set(["Emma", "Tom"])


def test_delete_index(client: FlaskClient) -> None:
    """测试 POST 请求, 删除一个名词内容"""

    resp = client.post(
        "/",
        data={  # 通过 data 发送 form 数据
            "name": "Alvin",
        },
    )
    assert resp.status_code == 302
    assert resp.headers.get("Location") == "/"

    # 发送 DELETE 请求
    resp = client.delete(f'/?value={quote("Alvin")}')

    assert resp.status_code == 302
    assert resp.headers.get("Location") == "/"

    assert set(get_names()) == set()


def test_get_index(client: FlaskClient) -> None:
    """测试 GET 请求, 添加一个名词内容"""

    resp = client.post(
        "/",
        data={  # 通过 data 发送 form 数据
            "name": "Alvin",
        },
    )
    assert resp.status_code == 302

    # 发送 GET 请求, 获取 / 返回的 HTML 内容
    resp = client.get(resp.headers.get("Location"))
    assert resp.status_code == 200
    assert b'<span class="content">Alvin</span>' in resp.data
