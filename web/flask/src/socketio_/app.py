from utils.trace import is_debug

if not is_debug():
    from gevent import monkey

    monkey.patch_all()

from multiprocessing import RLock
from typing import Any, Dict, List, Tuple

from flask_socketio import SocketIO, disconnect, join_room, leave_room
from utils.paths import get_watch_files_for_develop
from utils.trace import attach_logger
from utils.web import Assets, templated

from flask import Flask, request

# 实例化 Flask 对象
app = Flask(__name__, static_folder="static", template_folder="templates")

# 为 jinja 注入 assets 对象实例
app.jinja_env.globals["assets"] = Assets(app)

# 设置安全密钥
app.config["SECRET_KEY"] = "secret!!!"

_TOKEN = (
    "olriajpjatxhhyptgllgrrhuvukhkkbsqrekmeexioeqwkewinhuowzhiakiebxnot"
    "fqthnrkhdfrccmqvljmzeymjlkfkdoveavbddsfsewxhrezyxlufdzczbumlztjnpz"
    "gcgjtlkuakdmwtznlonxtwikzpbttzhrynrremoucsgexzpriytvdjgqeejyvtkncd"
    "rzkicaawapmuwfgloldnwvlkscjriragsiwdifswasceelxnonlwtbfqvi"
)

_NAMESPACE = "/my-chat"

_ROOMS: Dict[str, List[Tuple[str, str]]] = {}

_lock = RLock()

# 实例化 socketio 对象
sio = SocketIO(
    app,
    engineio_logger=True,
    manage_session=False,
    cors_allowed_origins="*",
)
# sio.init_app(app)


@app.route("/", methods=["GET"])
@templated()
def index() -> Dict[str, Any]:
    """
    获取主页页面
    """
    app.logger.debug("Hello")
    return {"token": _TOKEN}


@sio.on("connect", namespace=_NAMESPACE)
def on_connect(auth: Dict[str, Any]) -> None:
    sid: str = request.sid  # type: ignore
    app.logger.info(f'A socketio client was connected as "{sid}"')

    if auth.get("token", "") != _TOKEN:
        app.logger.info(f'A socketio client ("{sid}") has invalid token, disconnected')
        disconnect(sid)


def emit_rooms_event() -> None:
    sio.emit("rooms", {"result": {"rooms": list(_ROOMS.keys())}}, namespace=_NAMESPACE)


@sio.on("rooms", namespace=_NAMESPACE)
def on_rooms() -> None:
    with _lock:
        emit_rooms_event()


@sio.on("joinRoom", namespace=_NAMESPACE)
def on_join_room(data: Dict[str, Any]) -> None:
    with _lock:
        room_name: str = data.get("roomName", "")
        if not room_name:
            sio.emit(
                "joinRoom",
                {"result": {"error": "Invalid room name"}},
                namespace=_NAMESPACE,
            )

        user_name: str = data.get("userName", "")
        if not user_name:
            sio.emit(
                "joinRoom",
                {"result": {"error": "Invalid user name"}},
                namespace=_NAMESPACE,
            )

        sid: str = request.sid  # type: ignore

        if room_name not in _ROOMS:
            _ROOMS[room_name] = []

            _ROOMS[room_name].append((sid, user_name))
            join_room(room_name, sid, namespace=_NAMESPACE)
        else:
            if (sid, user_name) not in _ROOMS[room_name]:
                _ROOMS[room_name].append((sid, user_name))
                join_room(room_name, sid, namespace=_NAMESPACE)
            else:
                sio.emit(
                    "joinRoom",
                    {"result": {"error": "User already in the room"}},
                    namespace=_NAMESPACE,
                )
                return

        emit_rooms_event()


@sio.on("leaveRoom", namespace=_NAMESPACE)
def on_leave_room(data: Dict[str, Any]) -> None:
    with _lock:
        room_name: str = data.get("roomName", "")
        if not room_name:
            sio.emit(
                "leaveRoom",
                {"result": {"error": "Invalid room name"}},
                namespace=_NAMESPACE,
            )

        sid: str = request.sid  # type: ignore

        if room_name not in _ROOMS:
            _ROOMS[room_name] = []

        _ROOMS[room_name] = [
            (sid, user_name) for sid, user_name in _ROOMS[room_name] if sid != sid
        ]
        leave_room(room_name, sid, namespace=_NAMESPACE)

        emit_rooms_event()


# 暴露给 wsgi 服务器的应用对象
flask_app = app

if __name__ == "__main__":
    # 进程启动时执行
    sio.run(
        app=app,
        host="127.0.0.1",
        port=5001,
        debug=True,
        extra_files=get_watch_files_for_develop(app),
    )
else:
    # 调试模式下执行
    flask_app = attach_logger(app)
