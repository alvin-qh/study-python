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
    assert (
        """
              <p>春之女神着素装，</p>
              <p>山楂花冠乳白光；</p>
              <p>天上分明一群羊，</p>
              <p>白云朵朵自来往；</p>
              <p>粉蝶空中时蹁跹；</p>
              <p>廷命菊花饰郊原；</p>
              <p>樱桃梨树共争艳，</p>
              <p>四处非花如雪片。</p>
"""
        in html
    )


def test_i18n_en_US(client: FlaskClient) -> None:
    resp = client.get("/?lang=en_US")

    assert resp.status_code == 200

    html = resp.data.decode("utf-8")
    assert "Spring Goeth All in White" in html
    assert "Robert Bridges" in html
    assert (
        """
              <p>Spring goeth all in white,</p>
              <p>crowned with milk-white may;</p>
              <p>In fleecy flocks of light,</p>
              <p>o'er heaven the white clouds stray;</p>
              <p>White butterflies in the air;</p>
              <p>White daisies prank the ground;</p>
              <p>The cherry and hoary pear,</p>
              <p>Scatter their snow around.</p>
"""
        in html
    )
