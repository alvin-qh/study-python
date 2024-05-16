from utils.trace import is_debug

if not is_debug():
    from gevent import monkey

    monkey.patch_all()

from typing import Any, Dict, Tuple, Union

from utils.paths import get_watch_files_for_develop
from utils.trace import attach_logger
from utils.web import Assets, templated
from werkzeug import Response
from wtforms import DecimalField, Form, SelectField, validators

from flask import Flask, jsonify, request

# 实例化 Flask 对象
app = Flask(__name__, static_folder="static", template_folder="templates")

# 设置密钥
app.config["SECRET_KEY"] = "secret!!!"

# 为 jinja 注入 assets 对象
app.jinja_env.globals["assets"] = Assets(app)


class ExpressForm(Form):
    """Flask use WT-Forms to validate form

    See also: http://wtforms.readthedocs.io/en/stable/index.html
    """

    a = DecimalField(
        label="a",
        validators=[validators.data_required(message="Number a required")],
    )

    b = DecimalField(
        label="b",
        validators=[validators.data_required(message="Number b required")],
    )

    op = SelectField(
        label="op",
        choices=[
            ["+", "+"],
            ["-", "-"],
            ["*", "*"],
            ["/", "/"],
        ],
        validate_choice=False,
        validators=[
            validators.any_of(
                values=["+", "-", "*", "/"],
                message='Operator must on of "+. -, *, /"',
            ),
        ],
    )


# 计算函数字典
_OPS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}


@app.route("/", methods=["GET", "POST"])
@templated()
def index() -> Tuple[Dict[str, Any], int]:
    """对 GET / 和 POST / 进行路由处理

    GET /  获取计算器页面
    POST / 发送计算表单, 返回计算结果
    """
    ans = ""
    code = 200

    # 请求中的 form 内容实例化 Form 对象
    form = ExpressForm(request.form)

    if request.method == "POST":
        # 验证表单并进行计算
        if form.validate():
            ans = _OPS[form.op.data](float(form.a.data), float(form.b.data))
        else:
            code = 400

    # 返回表单结果
    return {"form": form, "ans": ans}, code


@app.route("/ajax", methods=["POST"])
def ajax() -> Union[Response, Tuple[Response, int]]:
    """处理 Ajax 类型请求

    通过 Ajax 请求发送计算表单, 获取计算结果
    """

    # 请求内容以 json 形式实例化 Form 对象
    form = ExpressForm(data=request.json)

    if not form.validate():
        return jsonify(errors=form.errors), 400

    ans = _OPS[form.op.data](float(form.a.data), float(form.b.data))
    return jsonify(ans=ans)


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
