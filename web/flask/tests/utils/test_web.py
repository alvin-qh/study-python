import json
from typing import Any, Dict
from unittest.mock import MagicMock, patch
from utils.web import templated, Assets
from flask import Flask


@patch("utils.web.render_template")
def test_templated_decorator_with_template_name(
    mocked_render_template: MagicMock,
) -> None:
    """测试通过命名模板调用装饰器"""

    @templated("demo/demo-template.html")
    def demo_template() -> Dict[str, Any]:
        return {"name": "demo"}

    demo_template()
    mocked_render_template.assert_called_once_with(
        "demo/demo-template.html", name="demo"
    )


@patch("utils.web.render_template")
def test_templated_decorator_without_template_name(
    mocked_render_template: MagicMock,
) -> None:
    """测试通过未命名模板调用装饰器"""

    @templated()
    def demo_template() -> Dict[str, Any]:
        return {"name": "demo"}

    with Flask(__name__).test_request_context():
        with patch("utils.web.request") as mocked_request:
            mocked_request.endpoint = "demo.index"

            demo_template()
            mocked_render_template.assert_called_once_with(
                "demo/index.html", name="demo"
            )


@patch("utils.web.open")
@patch("utils.web.os")
def test_assets_with_manifest(mocked_os: MagicMock, mocked_open: MagicMock) -> None:
    """测试在具备 `manifest.json` 文件的情况下, 获取静态文件路径和文件名"""

    mocked_os.path.join.return_value = "mocked/manifest.json"
    mocked_os.path.exists.return_value = True

    # mock 读取 "manifest.json" 文件, 返回文件 hash 缓存
    # mock 路径如下: open(...) as fp / fp.read(...)
    mocked_open.return_value.__enter__.return_value.read.return_value = json.dumps(
        {
            "images/demo/demo.png": "images/demo/demo.png?__v=abcdef",
            "script/demo/demo.js": "script/demo/demo.js?__v=xyzddd",
            "css/demo/demo.css": "css/demo/demo.css?__v=deadbeef",
        }
    )

    app = Flask(__name__)

    with app.test_request_context():
        assets = Assets(app)
        assert (
            assets.image("demo/demo.png") == "/static/images/demo/demo.png?__v=abcdef"
        )
        assert assets.script("demo/demo.js") == "/static/script/demo/demo.js?__v=xyzddd"
        assert assets.css("demo/demo.css") == "/static/css/demo/demo.css?__v=deadbeef"


@patch("utils.web.open")
@patch("utils.web.os")
def test_assets_without_manifest(mocked_os: MagicMock, mocked_open: MagicMock) -> None:
    """测试没有 manifest.json 文件时, 会根据文件内容计算 hash 值"""

    # 返回表示 manifest.json 文件不存在
    mocked_os.path.exists.return_value = False

    # 返回表示静态文件存在
    mocked_os.path.isfile.return_value = True

    # 返回静态文件内容
    mocked_open.return_value.__enter__.return_value.read.return_value = b"abcdexyz"

    app = Flask(__name__)

    with app.test_request_context():
        assets = Assets(app)
        assert (
            assets.script("demo/demo.js")
            == "/static/script/demo/demo.js?__v=15e832ae2d7993d1"
        )
