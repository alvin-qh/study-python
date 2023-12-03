from utils.trace import is_debug

if not is_debug():
    from gevent import monkey

    monkey.patch_all()

from utils import Assets, attach_logger, get_watch_files_for_develop

from flask import Flask

# 创建 Flask 实例对象
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
)

# 在 jinja 模板中增加 assets 对象
app.jinja_env.globals["assets"] = Assets(app)


def register_blueprint() -> None:
    """
    注册 blueprint 对象
    """

    from blueprint.home import bp as home_bp
    from blueprint.user import bp as user_bp

    app.register_blueprint(home_bp, url_prefix="/")
    app.register_blueprint(user_bp, url_prefix="/user")


# 注册 blueprint
register_blueprint()


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
