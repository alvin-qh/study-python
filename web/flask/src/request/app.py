from utils.trace import is_debug

if not is_debug():
    from gevent import monkey

    monkey.patch_all()

from typing import Any, Callable, Dict, List, Set, Union

from utils.paths import get_watch_files_for_develop
from utils.trace import attach_logger
from utils.web import Assets, HttpMethodOverrideMiddleware, templated
from werkzeug import Response
from werkzeug.exceptions import BadRequest

from flask import Flask, redirect, request

# 实例化 Flask 对象
app = Flask(__name__, static_folder="static", template_folder="templates")

# 设置 http 请求方法重写中间件对象
app.wsgi_app = HttpMethodOverrideMiddleware(app.wsgi_app)  # type: ignore

# 为 jinja 注入 assets 对象
app.jinja_env.globals["assets"] = Assets(app)

# 保存输入内容的 set 集合
_NAMES: Set[str] = set()


def _search_result() -> Dict[str, Any]:
    """根据查询参数查询结果

    Returns:
        `Dict[str, Any]`: 查询结果
    """

    # 获取查询参数
    kwd = request.args.get("kwd", "")
    if kwd:
        # 查询匹配的结果
        results = list(filter(lambda n: n.find(kwd) >= 0, _NAMES))
    else:
        # 获取全部结果
        results = list(_NAMES)

    # 返回查询结果
    return {"name": kwd, "results": results}


def _add_name() -> Response:
    """增加查询项

    Returns:
        `Response`: 重定向响应结果
    """

    # 从请求的表单中获取要增加的项
    name = request.form.get("name")
    if name:
        # 增加
        _NAMES.add(name)

    return redirect("/")


def _change_name() -> Response:
    """修改查询项

    Raises:
        `BadRequest`: 请求参数不合法

    Returns:
        `Response`: 重定向响应结果
    """

    # 获取原有的查询项值并删除
    old_value = request.form.get("old_value")
    if old_value in _NAMES:
        _NAMES.remove(old_value)

    # 增加新的查询项值
    new_value = request.form.get("new_value")
    if not new_value:
        raise BadRequest("invalid form data")

    _NAMES.add(new_value)

    return redirect("/")


def _delete_name() -> Response:
    """删除查询项

    Returns:
        `Response`: 重定向响应结果
    """

    value = request.args.get("value")
    if value in _NAMES:
        _NAMES.remove(value)

    return redirect("/")


# 请求方法和处理函数字典
_METHOD_MAP: Dict[str, Callable[[], Union[Dict[str, Any], Response]]] = {
    "GET": _search_result,
    "POST": _add_name,
    "PUT": _change_name,
    "DELETE": _delete_name,
}


@app.route("/", methods=["GET", "POST", "PUT", "DELETE"])
@templated()
def index() -> Union[Dict[str, Any], Response]:
    """根据不同的请求类型, 执行不同的操作

    Returns:
        `Union[Dict[str, Any], Response]`: 响应结果
    """
    return _METHOD_MAP[request.method]()


def get_names() -> List[str]:
    """获取保存的名称集合"""
    return list(_NAMES) if _NAMES else []


def clear_names() -> None:
    """清空保存的名称集合"""
    global _NAMES
    _NAMES = set()


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
