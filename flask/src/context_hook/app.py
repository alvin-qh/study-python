from utils.trace import is_debug

if not is_debug():
    from gevent import monkey

    monkey.patch_all()

from typing import Any, Dict, Optional, Tuple, Union

from utils import Assets, attach_logger, get_watch_files_for_develop, templated
from werkzeug import Response
from wtforms import Form, PasswordField, StringField, validators

from flask import Flask, g, redirect, request, session


class User:
    """
    定义用户类
    """

    def __init__(self, name: str, gender: str, password: str) -> None:
        self.name = name
        self.gender = gender
        self.password = password


# 系统内置用户集合
USERS = {
    1: User("Alvin", "M", "123456"),
    2: User("Emma", "F", "888888"),
}


# 创建 Flask 实例
app = Flask(__name__, template_folder="templates", static_folder="static")

# 设置加密密钥
app.config[
    "SECRET_KEY"
] = b"?\xc0\xa9\xfcY\xd7\x9f+\xbe\n\x85\x16\xa0\xd9\xaa\x9fG\x14\x0e\xeb\xf4\x05N\xe3"

# 为 jinja 增加 assets 对象
app.jinja_env.globals["assets"] = Assets(app)


def before_request() -> Optional[Response]:
    """定义请求钩子

    在每次请求处理前, 检查用户是否登录
    """

    # 对于访问静态资源或者登陆页面，不进行拦截
    if request.endpoint in {"static", "login"}:
        return None

    # 判断 session 中是否包含登录信息
    if "user_id" not in session:
        return redirect("/login")

    # 获取 session 中存储的 user_id 信息
    user_id = session["user_id"]

    # 判断用户是否存在
    user = USERS[user_id]
    if not user:
        return redirect("/login")

    # 在请求上下文中保持登录信息
    g.user = user
    return None


# 注册 hook，在每次请求前执行 check_login 函数
app.before_request(before_request)

"""
也可以通过装饰器方式进行

@app.before_request
def before_request():
    ...
"""


class LoginForm(Form):
    """登录的 Form 类型"""

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
    return {"user": g.user}


@app.route("/login", methods=["GET", "POST"])
@templated()
def login() -> Union[Response, Tuple[Union[Response, Dict[str, Any]], int]]:
    """处理 GET /login 和 POST /login 路由

    GET 请求展示登录页
    POST 请求发送登录表单进行登录
    """

    # 创建登录信息表单
    form = LoginForm(request.form)

    # 判断是否以 POST 方式访问
    # POST 表示提交表单
    # GET 表示获取表单填写页面
    if request.method == "POST":
        # 判断表单验证结果
        if not form.validate():
            return {"form": form}, 400

        # 获取用户名
        account = form.account.data

        # 获取密码
        password = form.password.data

        # 查询用户是否存在
        find_user = next(
            filter(
                lambda item: (account or "").lower() == item[1].name.lower(),
                USERS.items(),
            ),
            None,
        )

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

    return {"form": form}, 400 if form.errors else 200


@app.route("/logout", methods=["POST"])
@templated()
def logout() -> dict[str, Any]:
    """处理 POST /logout 路由

    处理登出请求
    """
    # 从请求上下文中获取当前登录用户
    user: User = g.user

    # 清理 session
    session.clear()
    return {"user": user}


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
