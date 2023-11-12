from flask.testing import FlaskClient
import pytest
from basic import app


@pytest.fixture(scope="module")
def client() -> FlaskClient:
    """定义获取 Flask 测试客户端的 fixture"""
    return app.test_client()


def test_get_index(client: FlaskClient) -> None:
    """测试 GET / 路由调用"""

    resp = client.get("/")
    assert (
        resp.data
        == b"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>Hello</title>
</head>
<body>
  <h1>Hello World</h1>
  <a href="/template">Next</a>
</body>
</html>
"""
    )
