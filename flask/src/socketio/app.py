import logging
from typing import Any, Dict

from flask_socketio import SocketIO, disconnect
from utils import Assets, get_watch_files_for_develop, templated

from flask import Flask, request

# 实例化 Flask 对象
app = Flask(__name__, static_folder="static", template_folder="templates")

# 为 jinja 注入 assets 对象实例
app.jinja_env.globals["assets"] = Assets(app)

# 设置安全密钥
app.config["SECRET_KEY"] = "secret!"

_TOKEN = (
    "olriajpjatxhhyptgllgrrhuvukhkkbsqrekmeexioeqwkewinhuowzhiakiebxnot"
    "fqthnrkhdfrccmqvljmzeymjlkfkdoveavbddsfsewxhrezyxlufdzczbumlztjnpz"
    "gcgjtlkuakdmwtznlonxtwikzpbttzhrynrremoucsgexzpriytvdjgqeejyvtkncd"
    "rzkicaawapmuwfgloldnwvlkscjriragsiwdifswasceelxnonlwtbfqvi"
)

# 实例化 socketio 对象
sio = SocketIO(
    app,
    engineio_logger=True,
    cors_allowed_origins="*",
)
sio.init_app(app)


@app.route("/", methods=["GET"])
@templated()
def index() -> Dict[str, Any]:
    """
    获取主页页面
    """
    app.logger.debug("Hello")
    return {"token": _TOKEN}


@sio.on("connect", namespace="/mychat")
def on_connect(auth: Dict[str, Any]) -> None:
    sid: str = request.sid  # type: ignore
    app.logger.info(f'A socketio client was connected as "{sid}"')

    if auth.get("token", "") != _TOKEN:
        app.logger.info(f'A socketio client ("{sid}") has invalid token, disconnected')
        disconnect(sid)


@sio.on("aaa", namespace="/mychat")
def on_message(msg: Dict[str, Any], args: Any) -> None:
    pass


def main() -> None:
    # 通过 socketio 启动 flask 应用
    sio.run(
        app,
        host="127.0.0.1",
        port=5001,
        debug=False,
        extra_files=get_watch_files_for_develop(app),
    )


if __name__ == "__main__":
    main()
else:
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
