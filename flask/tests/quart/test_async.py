from typing import Any, Dict, cast

import pytest
from quart.testing import QuartClient
from quart_ import app


@pytest.fixture(scope="module")
def client() -> QuartClient:
    """定义获取 Flask 测试客户端的 fixture"""
    return cast(QuartClient, app.test_client())


@pytest.mark.asyncio
async def test_get_index(client: QuartClient) -> None:
    """测试 GET / 路由调用"""

    resp = await client.get("/")

    assert resp.status_code == 200
    assert b'<script src="/static/script/show-time.js"></script>' in await resp.data


@pytest.mark.asyncio
async def test_get_json(client: QuartClient) -> None:
    """测试 GET /json 路由调用"""

    resp = await client.get("/json")

    assert resp.status_code == 200

    json_data: Dict[str, Any] = cast(Dict[str, Any], await resp.json)
    assert "time" in json_data
    assert isinstance(json_data["time"], int)
