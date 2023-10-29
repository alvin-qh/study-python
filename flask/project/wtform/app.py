from typing import Any, Dict

from flask import Flask, jsonify, request
from werkzeug import Response
from wtforms import DecimalField, Form, SelectField, validators

from utils import Assets, templated, watch_files_for_develop

# 实例化 Flask 对象
app = Flask(__name__, static_folder="static", template_folder="templates")
# 设置密钥
app.config[
    "SECRET_KEY"
] = b"?\xc0\xa9\xfcY\xd7\x9f+\xbe\n\x85\x16\xa0\xd9\xaa\x9fG\x14\x0e\xeb\xf4\x05N\xe3"
# 为 jinja 注入 assets 对象
app.jinja_env.globals["assets"] = Assets(app)


class ExpressForm(Form):
    """
    Flask use WT-Forms to validate form
    See also: http://wtforms.readthedocs.io/en/stable/index.html
    """

    a = DecimalField(
        label="a", validators=[validators.data_required(message="Number a required")]
    )

    b = DecimalField(
        label="b", validators=[validators.data_required(message="Number b required")]
    )

    op = SelectField(
        label="op",
        choices=(("+", "+"), ("-", "-"), ("*", "*"), ("/", "/")),
        validators=[
            validators.any_of(
                values=["+", "-", "*", "/"], message='Operator must on of "+. -, *, /"'
            ),
        ],
    )


_OPS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}


@app.route("/", methods=["GET", "POST"])
@templated()
def index() -> Dict[str, Any]:
    """
    获取主页页面
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
    return dict(form=form, ans=ans), code


@app.route("/ajax", methods=["POST"])
def ajax() -> Response:
    """
    处理 Ajax 类型请求
    """

    # 请求内容以 json 形式实例化 Form 对象
    form = ExpressForm(data=request.json)

    if not form.validate():
        return jsonify(errors=form.errors), 400

    ans = _OPS[form.op.data](float(form.a.data), float(form.b.data))
    return jsonify(ans=ans)


if __name__ == "__main__":
    # 启动 flask 应用
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        extra_files=watch_files_for_develop(app),
    )
