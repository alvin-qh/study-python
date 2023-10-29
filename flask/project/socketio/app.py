from typing import Any, Dict
from flask import Flask
from flask_socketio import SocketIO

from utils import Assets, templated, watch_files_for_develop

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
    return dict()


if __name__ == "__main__":
    # 通过 socketio 启动 flask 应用
    sio.run(
        app,
        host="127.0.0.1",
        port=5000,
        debug=True,
        extra_files=watch_files_for_develop(app),
    )
