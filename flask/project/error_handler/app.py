from typing import Any, Dict

from flask import Flask, render_template

from utils import Assets, templated, watch_files_for_develop

# 创建 Flask 应用实例
app = Flask(__name__, template_folder="templates", static_folder="static")
# 为 jinja 注入 assets 对象
app.jinja_env.globals["assets"] = Assets(app)


class NothingError(Exception):
    """
    定义测试用的异常类
    """
    pass


@app.route("/", methods=["GET"])
@templated()
def index() -> Dict[str, Any]:
    """
    获取主页页面
    """
    return dict()


@app.route("/exception", methods=["GET"])
def exception() -> None:
    """
    抛出异常
    """
    raise NothingError("Oh shit!!")


@app.errorhandler(404)
def error_404(err):
    """
    处理 404 错误，渲染错误页面
    """
    return render_template(
        "error-page.html",
        msg="Page was gone with wind",
        err=err,
    ), 404


@app.errorhandler(NothingError)
def error_exception(err):
    """
    处理 NothingError 异常，渲染错误页面
    """
    return render_template(
        "error-page.html",
        msg="Exception was caused",
        err=err,
    ), 500


if __name__ == "__main__":
    # 启动 flask 应用
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        extra_files=watch_files_for_develop(app),
    )
