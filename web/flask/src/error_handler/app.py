from utils.trace import is_debug

if not is_debug():
    from gevent import monkey

    monkey.patch_all()

from traceback import format_tb
from typing import Any, Dict, NoReturn, Tuple

from utils.paths import get_watch_files_for_develop
from utils.trace import attach_logger
from utils.web import Assets, templated

from flask import Flask, render_template

# 创建 Flask 应用实例
app = Flask(__name__, template_folder="templates", static_folder="static")

# 为 jinja 注入 assets 对象
app.jinja_env.globals["assets"] = Assets(app)


class NothingError(Exception):
    """定义测试用的异常类"""


@app.route("/", methods=["GET"])
@templated()
def index() -> Dict[str, Any]:
    """获取主页页面"""
    return dict()


@app.route("/exception", methods=["GET"])
def exception() -> NoReturn:
    """抛出异常"""
    raise NothingError("Oh shit!!")


@app.errorhandler(404)
def error_404(err: int) -> Tuple[str, int]:
    """处理 404 错误，渲染错误页面"""
    return (
        render_template(
            "error-page.html",
            msg="Page was gone with wind",
            err=err,
        ),
        404,
    )


@app.errorhandler(NothingError)
def error_exception(err: NothingError) -> Tuple[str, int]:
    """处理 NothingError 异常，渲染错误页面"""
    return (
        render_template(
            "error-page.html",
            msg="Exception was caused",
            err=str(err),
            stack_trace=format_tb(err.__traceback__),
        ),
        500,
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
