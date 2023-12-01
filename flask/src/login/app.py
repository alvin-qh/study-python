from typing import Tuple, Union

from flask_login import LoginManager
from login.form import LoginForm
from login.model import UserModel
from utils.paths import get_watch_files_for_develop
from utils.web import Assets
from werkzeug.wrappers import Response

from flask import Flask, redirect, render_template, request

# 创建 Flask 应用实例
app = Flask(__name__, template_folder="templates", static_folder="static")

# 设置应用密钥，用于加密 cookie 和 session 数据
app.config["SECRET_KEY"] = "secret!!!"

# 为 jinja 注入 assets 对象
app.jinja_env.globals["assets"] = Assets(app)

# 实例化登陆管理器
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(user_id: int) -> UserModel:
    return UserModel.get(user_id)


@app.route("/login", methods=["GET", "POST"])
def login() -> Union[Tuple[str, int], Response]:
    if request.method == "GET":
        return render_template("login.html", form=LoginForm()), 200
    else:
        form = LoginForm(request.form)
        if not form.validate():
            return render_template("login.html", form=LoginForm()), 400

        user = UserModel.find_by_name(form.username)
        if user is None:
            return render_template("login.html"), 403

        if user.password != form.password:
            return render_template("login.html"), 403

        return redirect("/")


def main() -> None:
    # 启动 flask 应用
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        extra_files=get_watch_files_for_develop(app),
    )


if __name__ == "__main__":
    main()