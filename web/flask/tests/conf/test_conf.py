from typing import cast

import pytest
from conf import app

from flask.testing import FlaskClient


@pytest.fixture(scope="module")
def client() -> FlaskClient:
    """定义获取 Flask 测试客户端的 fixture"""
    return cast(FlaskClient, app.test_client())


def test_get_index(client: FlaskClient) -> None:
    """测试 POST 请求, 添加一个名词内容"""

    resp = client.get("/")
    assert resp.status_code == 200
    assert b"<th>SECRET_KEY</th>" in resp.data
    assert (
        b"<td>b&#39;?\\xc0\\xa9\\xfcY\\xd7\\x9f+\\xbe\\n\\x85\\x16\\xa0\\xd9"
        b"\\xaa\\x9fG\\x14\\x0e\\xeb\\xf4\\x05N\\xe3&#39;</td>"
    ) in resp.data
