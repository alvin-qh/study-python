from utils.trace import is_debug

if not is_debug():
    from gevent import monkey

    monkey.patch_all()

from typing import Any, Dict, Tuple

from utils import Assets, attach_logger, get_watch_files_for_develop, templated
from werkzeug import Response

from flask import Flask, jsonify, request

# 实例化 Flask 对象
app = Flask(__name__, template_folder="templates", static_folder="static")

# 为 jinja 注入 assets 对象
app.jinja_env.globals["assets"] = Assets(app)

# 为 jinja 注入 url 函数
app.jinja_env.globals["url"] = lambda url: "/" + url


@app.route("/", methods=["GET"])
@templated("index.html")
def index() -> Dict[str, Any]:
    """
    获取主页页面
    """
    return {}


@app.route("/api/search", methods=["GET"])
def search() -> Tuple[Response, int]:
    """
    获取检索结果
    """
    key = request.args.get("key")
    if not key:
        return jsonify(message="Invalid key word"), 400

    return (
        jsonify(
            results=[
                {
                    "title": "Welcome | Jinja2 (The Python Template Engine)",
                    "description": "Jinja is a fast, expressive, extensible templating engine. "
                    "Special placeholders in the template allow writing code similar "
                    "to Python syntax. Then the template is passed data to render the "
                    "final document.",
                    "url": "http://jinja.pocoo.org",
                }
            ]
        ),
        200,
    )


# 暴露给 wsgi 服务器的应用对象
flask_app = app

if __name__ == "__main__":
    # 进程启动时执行
    flask_app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        extra_files=get_watch_files_for_develop(app),
    )
else:
    # 调试模式下执行
    flask_app = attach_logger(app)
