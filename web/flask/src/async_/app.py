from utils.trace import is_debug

if not is_debug():
    from gevent import monkey

    monkey.patch_all()

import time
from typing import Any, Dict, Tuple

from utils.paths import get_watch_files_for_develop
from utils.trace import attach_logger
from utils.web import async_templated
from werkzeug import Response

from flask import Flask, jsonify, request

# 实例化 Flask 对象
app = Flask(__name__, static_folder="static", template_folder="templates")

# 设置密钥
app.config["SECRET_KEY"] = "secret!!!"


@app.before_request
async def before_request() -> None:
    """在每次请求之前执行"""
    app.logger.info(
        "Request incoming, path=%s, from=%s", request.path, request.remote_addr
    )


@app.after_request
async def after_request(response: Response) -> Response:
    """在每次请求之后执行

    Args:
        - `response` (`Response`): 即将发给客户端的响应对象

    Returns:
        `Response`: 响应对象
    """
    response.headers.add("X-App-Id", "Flask-Async")

    # 输出响应信息
    app.logger.info(
        "Response outgo, status=%s, path=%s, to=%s",
        response.status_code,
        request.path,
        request.remote_addr,
    )
    return response


@app.route("/", methods=["GET"])
@async_templated()
async def index() -> Tuple[Dict[str, Any], int]:
    """处理异步请求

    该函数通过 `@async_templated` 注解, 在异步调用的基础上完成模板渲染
    """
    return {"message": "Async Route"}, 200


@app.route("/json", methods=["GET"])
async def use_json() -> Tuple[Response, int]:
    """处理异步 RESTful API 调用

    该函数通过
    """
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
