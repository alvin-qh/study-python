from typing import Any, Dict, Union

from flask import Flask, redirect, request
from werkzeug import Response

from utils import (Assets, HttpMethodOverrideMiddleware, templated,
                   watch_files_for_develop)

# 实例化 Flask 对象
app = Flask(__name__, static_folder="static", template_folder="templates")
# 设置 http 请求方法重写中间件对象
app.wsgi_app = HttpMethodOverrideMiddleware(app.wsgi_app)
# 为 jinja 注入 assets 对象
app.jinja_env.globals["assets"] = Assets(app)

# 保存输入内容的 set 集合
NAMES = set()


def _search_result() -> Dict[str, Any]:
    """
    根据查询参数查询结果
    """

    # 获取查询参数
    kwd = request.args.get("kwd", "")
    if kwd:
        # 查询匹配的结果
        results = list(filter(lambda n: n.find(kwd) >= 0, NAMES))
    else:
        # 获取全部结果
        results = list(NAMES)

    # 返回查询结果
    return dict(name=kwd, results=results)


def _add_name() -> Response:
    """
    增加查询项
    """
    # 从请求的表单中获取要增加的项
    name = request.form.get("name")
    if name:
        # 增加
        NAMES.add(name)

    return redirect("/")


def _change_name() -> Response:
    """
    修改查询项
    """
    # 获取原有的查询项值并删除
    old_value = request.form.get("old_value")
    if old_value in NAMES:
        NAMES.remove(old_value)

    # 增加新的查询项值
    new_value = request.form.get("new_value")
    NAMES.add(new_value)
    return redirect("/")


def _delete_name() -> Response:
    """
    删除查询项
    """
    value = request.args.get("value")
    if value in NAMES:
        NAMES.remove(value)

    return redirect("/")


@app.route("/", methods=["GET", "POST", "PUT", "DELETE"])
@templated()
def index() -> Union[Dict[str, Any], Response]:
    """
    根据不同的请求类型，执行不同的操作
    """
    return {
        "GET": _search_result,
        "POST": _add_name,
        "PUT": _change_name,
        "DELETE": _delete_name
    }[request.method]()


if __name__ == "__main__":
    # 启动 flask 应用
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        extra_files=watch_files_for_develop(app),
    )
