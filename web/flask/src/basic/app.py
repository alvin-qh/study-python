from utils.trace import is_debug

if not is_debug():
    from gevent import monkey

    monkey.patch_all()

import logging
import time
from typing import Any, Dict, Tuple

from utils.paths import get_watch_files_for_develop
from utils.trace import attach_logger
from utils.web import templated

from flask import Flask, Response, jsonify

# 创建 Flask 对象，并指定静态文件存储路径以及 html 模板存储路径
app: Flask = Flask(__name__, static_folder="static", template_folder="templates")

# 将 gunicorn 服务器的 log 接入到 flask log 中
gunicorn_logger = logging.getLogger("gunicorn.error")
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

# 定义 route


@app.route("/", methods=["GET"])
def index() -> Tuple[str, int]:
    """定义 GET / 路由方法"""

    return (
        """<!DOCTYPE html>
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
""",
        200,
    )


@app.route("/template", methods=["GET"])
@templated()
def template() -> Dict[str, Any]:
    """定义 GET /template 路由方法"""
    return {"data": {"title": "Hello", "message": "Hello World"}}


@app.route("/json", methods=["GET"])
def use_json() -> Tuple[Response, int]:
    """定义 GET /json 路由方法"""
    tm = time.mktime(time.localtime(time.time()))
    return jsonify(time=int(tm)), 200


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
