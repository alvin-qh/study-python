from typing import cast

import pytest
from i18n import app

from flask.testing import FlaskClient


@pytest.fixture(scope="module")
def client() -> FlaskClient:
    """定义获取 Flask 测试客户端的 fixture"""
    return cast(FlaskClient, app.test_client())


def test_i18n_zh_CN(client: FlaskClient) -> None:
    resp = client.get("/?lang=zh_CN")

    assert resp.status_code == 200

    html = resp.data.decode("utf-8")
    assert "春之女神着素装" in html
    assert "罗伯特·布里季" in html
    for txt in [
        "春之女神着素装",
        "山楂花冠乳白光",
        "天上分明一群羊",
        "白云朵朵自来往",
        "粉蝶空中时蹁跹",
        "廷命菊花饰郊原",
        "樱桃梨树共争艳",
        "四处非花如雪片",
    ]:
        assert txt in html


def test_i18n_en_US(client: FlaskClient) -> None:
    resp = client.get("/?lang=en_US")

    assert resp.status_code == 200

    html = resp.data.decode("utf-8")
    assert "Spring Goeth All in White" in html
    assert "Robert Bridges" in html
    for txt in [
        "Spring goeth all in white,",
        "crowned with milk-white may",
        "In fleecy flocks of light,",
        "o'er heaven the white clouds stray;",
        "White butterflies in the air;",
        "White daisies prank the ground;",
        "The cherry and hoary pear,",
        "Scatter their snow around.",
    ]:
        assert txt in html
