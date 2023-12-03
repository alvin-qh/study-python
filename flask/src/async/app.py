from utils.trace import is_debug

if not is_debug():
    from gevent import monkey

    monkey.patch_all()

import time
from typing import Any, Dict, Tuple

from utils import async_templated, attach_logger, get_watch_files_for_develop
from werkzeug import Response

from flask import Flask, jsonify

# 实例化 Flask 对象
app = Flask(__name__, static_folder="static", template_folder="templates")

# 设置密钥
app.config["SECRET_KEY"] = "secret-key!!!"


@app.route("/", methods=["GET"])
@async_templated()
async def index() -> Tuple[Dict[str, Any], int]:
    return {"message": "Async Route"}, 200


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
