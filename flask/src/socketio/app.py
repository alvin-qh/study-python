import logging
from typing import Any, Dict

from flask_socketio import SocketIO
from utils import Assets, get_watch_files_for_develop, templated

from flask import Flask

# 实例化 Flask 对象
app = Flask(__name__, static_folder="static", template_folder="templates")

# 为 jinja 注入 assets 对象实例
app.jinja_env.globals["assets"] = Assets(app)

# 设置安全密钥
app.config["SECRET_KEY"] = "secret!"

# 实例化 socketio 对象
sio = SocketIO(app, engineio_logger=True)


@app.route("/", methods=["GET"])
@templated()
def index() -> Dict[str, Any]:
    """
    获取主页页面
    """
    return {}


@sio.on("connect", namespace="/mychat")
def on_connect(auth: Dict[str, Any]) -> None:
    logging.info("connect: %s", auth)
    print("connect: %s", auth)


def main() -> None:
    # 通过 socketio 启动 flask 应用
    sio.run(
        app,
        host="127.0.0.1",
        port=5001,
        debug=True,
        extra_files=get_watch_files_for_develop(app),
    )


if __name__ == "__main__":
    main()
