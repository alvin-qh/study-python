from typing import Any, Dict, Optional

from flask import Flask, request, session
from flask_babel import Babel
from flask_babel import lazy_gettext as _
from flask_babel import refresh

from utils import Assets, templated, watch_files_for_develop

# 实例化 Flask 应用对象
app = Flask(__name__, static_folder="static", template_folder="templates")
app.jinja_env.globals["assets"] = Assets(app)
app.config.from_pyfile("conf.py")

# 实例化 Babel 对象
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    为每次请求匹配最佳的语言
    """
    lang = session.get("lang")
    if lang:
        return lang

    return request.accept_languages.best_match(app.config["BABEL_SUPPORT_LOCALES"], "zh_CN")


@babel.timezoneselector
def get_timezone() -> str:
    """
    为每次请求批评最佳的时区设置
    """
    zone = session.get("time_zone")
    if zone:
        return zone

    return "UTC"


@app.route("/", methods=["GET"])
@templated()
def index() -> Dict[str, Any]:
    """
    获取主页页面
    """
    # 获取请求中的 lang 参数
    lang = request.args.get("lang")
    if lang:
        # 参数值存入 session
        session["lang"] = lang
        # 刷新页面，更新语言
        refresh()
    else:
        lang = session.get("lang", "zh_CN")

    # 获取目前支持的语言列表
    langs = {"zh_CN": _("zh_CN"), "en_US": _("en_US")}

    return dict(current_lang=langs[lang])


if __name__ == "__main__":
    # 启动 flask 应用
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        extra_files=watch_files_for_develop(app),
    )
