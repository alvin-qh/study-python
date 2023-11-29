from typing import cast
from urllib.parse import quote

import pytest
from bs4 import BeautifulSoup
from jinja import app

from flask.testing import FlaskClient


@pytest.fixture(scope="module")
def client() -> FlaskClient:
    """定义获取 Flask 测试客户端的 fixture"""
    return cast(FlaskClient, app.test_client())


def test_get_home_index(client: FlaskClient) -> None:
    resp = client.get("/")
    assert resp.status_code == 200

    soup = BeautifulSoup(resp.data, "html.parser")

    assert soup.title and (soup.title.string or "").strip() == "Jinja Demo"
    assert [link["href"] for link in soup.select("head>link[rel=stylesheet]")] == [
        "/static/css/common-aca24d29.css",
        "/static/css/index-a7666c5b.css",
    ]

    assert [link["href"] for link in soup.select("head>link[rel='shortcut icon']")] == [
        "/static/images/favicon-adc8fbb1.ico",
    ]

    assert [img["src"] for img in soup.select("#app .title img")] == [
        "/static/images/logo-fb06e04c.png"
    ]

    assert [script["src"] for script in soup.select("body script")] == [
        "/static/script/common-b310268b.js",
        "/static/script/index-73c46e3e.js",
    ]


def test_search_result(client: FlaskClient) -> None:
    resp = client.get(f"/api/search?key={quote('python')}")
    assert resp.status_code == 200

    assert resp.json == {
        "results": [
            {
                "description": (
                    "Jinja is a fast, expressive, extensible "
                    "templating engine. Special placeholders in the "
                    "template allow writing code similar to Python "
                    "syntax. Then the template is passed data to "
                    "render the final document."
                ),
                "title": "Welcome | Jinja2 (The Python Template Engine)",
                "url": "http://jinja.pocoo.org",
            }
        ],
    }
