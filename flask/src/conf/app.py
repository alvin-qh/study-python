import os

from utils import Assets, get_watch_files_for_develop, templated

from flask import Config, Flask

# 创建 Flask 实例
app: Flask = Flask(__name__, template_folder="templates", static_folder="static")

app.jinja_env.globals["assets"] = Assets(app)

# 获取 ENV 环境变量
env = os.environ.get("ENV")

# 根据 ENV 环境变量加载不同的配置文件
if env:
    app.config.from_pyfile(f"conf_{env}.py")
else:
    app.config.from_pyfile("conf.py")


@app.route("/", methods=["GET"])
@templated()
def index() -> Config:
    """获取 Flask 配置信息的页面路由函数

    定义在 `conf.py` 文件中的变量会自动加入配置对象

    Returns:
        `Config`: Flask 配置对象
    """
    return app.config


def main() -> None:
    # 启动 flask 应用
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        extra_files=get_watch_files_for_develop(app),
    )


if __name__ == "__main__":
    # 启动 Flask 应用
    main()
