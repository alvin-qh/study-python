from utils.trace import is_debug

if not is_debug():
    from gevent import monkey

    monkey.patch_all()

from typing import Any, Dict, Optional

from flask_babel import Babel
from flask_babel import lazy_gettext as _
from flask_babel import refresh
from utils import Assets, attach_logger, get_watch_files_for_develop, templated

from flask import Flask, request, session

# 实例化 Flask 应用对象
app = Flask(__name__, static_folder="static", template_folder="templates")

# 为 jinja 注入 assets 对象
app.jinja_env.globals["assets"] = Assets(app)

# 加载配置文件
app.config.from_pyfile("conf.py")


def get_locale() -> str:
    """为每次请求匹配最佳的语言

    Returns:
        `str`: 语言代码
    """
    # 从用户上下文中获取语言设置
    lang: Optional[str] = session.get("lang")
    if lang:
        return lang

    # 匹配最适合的语言代码
    return request.accept_languages.best_match(
        app.config["BABEL_SUPPORT_LOCALES"],  # 从配置文件中读取默认语言配置
        "zh_CN",
    )


def get_timezone() -> str:
    """为每次请求批评最佳的时区设置

    Returns:
        `str`: 时区代码
    """
    # 从用户上下文中获取时区设置
    zone: Optional[str] = session.get("time_zone")
    if zone:
        return zone

    # 默认情况下使用 UTC 时区
    return "UTC"


# 实例化 Babel 对象
babel = Babel(app, locale_selector=get_locale, timezone_selector=get_timezone)
# babel.init_app(app, locale_selector=get_locale, timezone_selector=get_timezone)


@app.route("/", methods=["GET"])
@templated()
def index() -> Dict[str, Any]:
    """GET / 路由函数

    Returns:
        Dict[str, Any]: _description_
    """
    # 获取请求中的 lang 参数
    lang = request.args.get("lang", "")
    if lang:
        # 参数值存入 session
        session["lang"] = lang

        # 刷新页面，更新语言
        refresh()
    else:
        lang = session.get("lang", "zh_CN")

    # 获取目前支持的语言列表
    # `_` 函数是 `lazy_gettext` 函数的简写, 在使用 `pybabel extract` 命令时, 会将其放入多语言模板文件中
    langs = {"zh_CN": _("zh_CN"), "en_US": _("en_US")}

    # 返回语言代码
    return {"current_lang": langs.get(lang, _("zh_CN"))}


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
