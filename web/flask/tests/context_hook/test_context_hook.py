import re
from typing import cast

import pytest
from context_hook import app

from flask.testing import FlaskClient


@pytest.fixture(scope="module")
def client() -> FlaskClient:
    """定义获取 Flask 测试客户端的 fixture"""
    return cast(FlaskClient, app.test_client())


def test_redirect_without_login(client: FlaskClient) -> None:
    resp = client.get("/")

    assert resp.status_code == 302
    assert resp.location == "/login"


def test_login(client: FlaskClient) -> None:
    resp = client.post(
        "/login",
        data={
            "account": "Alvin",
            "password": "123456",
        },
    )

    assert resp.status_code == 302
    assert resp.location == "/"

    cookie = resp.headers["Set-Cookie"]
    assert re.match(r"^session=.+; HttpOnly; Path=/$", cookie)

    # 在请求中附加 cookie, 即可在请求钩子中通过 session 获取到登录数据
    resp = client.get("/", headers={"Set-Cookie": cookie})
    assert resp.status_code == 200

    html = resp.data.decode("utf-8")
    assert "Welcome Mr Alvin" in html


def test_logout(client: FlaskClient) -> None:
    resp = client.post(
        "/login",
        data={
            "account": "Alvin",
            "password": "123456",
        },
    )

    # 进行一次登录, 获取 cookie
    cookie = resp.headers["Set-Cookie"]

    # 带上登录 cookie, 请求登出
    resp = client.post("/logout", headers={"Set-Cookie": cookie})

    assert resp.status_code == 200

    html = resp.data.decode("utf-8")
    assert "Bye, Mr Alvin" in html

    # 服务端返回 cookie 清除设置
    assert re.match(
        "session=; Expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; HttpOnly; Path=/",
        resp.headers["Set-Cookie"],
    )
