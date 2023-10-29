from typing import Any, Dict

from flask import Flask, g, redirect, request, session
from wtforms import Form, PasswordField, StringField, validators

from utils import Assets, templated, watch_files_for_develop


class User:
    """
    定义用户类
    """

    def __init__(self, name: str, gender: str, password: str):
        self.name = name
        self.gender = gender
        self.password = password


# 系统内置用户集合
USERS = {
    1: User("Alvin", "M", "123456"),
    2: User("Emma", "F", "888888")
}


# 创建 Flask 实例
app = Flask(__name__, template_folder="templates", static_folder="static")
# 设置加密密钥
app.config["SECRET_KEY"] = b"?\xc0\xa9\xfcY\xd7\x9f+\xbe\n\x85\x16\xa0\xd9\xaa\x9fG\x14\x0e\xeb\xf4\x05N\xe3"
# 为 jinja 增加 assets 对象
app.jinja_env.globals["assets"] = Assets(app)


def check_login() -> None:
    """
    检查用户是否登录
    """

    # 对于访问静态资源或者登陆页面，不进行拦截
    if request.endpoint in {"static", "login"}:
        return

    # 判断 session 中是否包含登录信息
    if "user_id" not in session:
        return redirect("/login")

    # 获取 session 中存储的 user_id 信息
    user_id = session["user_id"]

    # 判断用户是否存在
    user = USERS[user_id]
    if not user:
        return redirect("/login")

    # 在上下文中保持登录信息
    g.user = user


# 注册 hook，在每次请求前执行 check_login 函数
app.before_request(check_login)

"""
也可以通过装饰器方式进行

@app.before_request
def check_login():
    if request.endpoint != "login" and "user_id" not in session
        return redirect("/login")
"""


class LoginForm(Form):
    """
    登录的 Form 类型
    """

    # 账号字段
    account = StringField(
        label="Account",
        validators=[
            validators.data_required(message="Account required"),
            validators.length(
                min=2,
                max=20,
                message="Account length must between 6 and 20",
            ),
        ],
    )

    # 密码字段
    password = PasswordField(
        label="Password",
        validators=[
            validators.data_required(message="Password required"),
            validators.length(
                min=6,
                max=20,
                message="Account length must between 6 and 20",
            ),
        ],
    )


@app.route("/", methods=["GET"])
@templated()
def index() -> Dict[str, Any]:
    """
    访问首页，如果正常登陆过，则返回当前用户信息
    """
    return dict(user=g.user)


@app.route("/login", methods=["GET", "POST"])
@templated()
def login():
    """
    登录页
    """

    # 创建登录信息表单
    form = LoginForm(request.form)

    # 判断是否以 POST 方式访问
    # POST 表示提交表单
    # GET 表示获取表单填写页面
    if request.method == "POST":
        # 判断表单验证结果
        if form.validate():
            # 获取用户名
            account = form.account.data
            # 获取密码
            password = form.password.data

            # 查询用户是否存在
            find_user = next(filter(lambda item: account ==
                             item[1].name, USERS.items()), None)
            if find_user:
                # 判断密码是否正确
                if find_user[1].password == password:
                    # 在 session 中存储用户信息
                    session["user_id"] = find_user[0]
                    return redirect("/")
                else:
                    form.password.errors = ["Invalid password"]
            else:
                form.account.errors = ["User not exits"]

    #
    return dict(form=form), 400 if form.errors else 200


@app.route("/logout", methods=["POST"])
@templated()
def logout():
    user = g.user
    session.clear()
    return dict(user=user)


if __name__ == "__main__":
    # 启动 flask 应用
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        extra_files=watch_files_for_develop(app),
    )
