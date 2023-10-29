from flask import Flask

from utils import Assets, watch_files_for_develop

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
    from home import bp as home_bp
    from user import bp as user_bp

    app.register_blueprint(home_bp, url_prefix="/")
    app.register_blueprint(user_bp, url_prefix="/user/")


# 注册 blueprint
register_blueprint()

if __name__ == "__main__":
    # 启动 flask 应用
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        extra_files=watch_files_for_develop(app),
    )
