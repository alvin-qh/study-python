import os

from flask import Flask

from utils import Assets, templated, watch_files_for_develop

# 创建 Flask 实例
app = Flask(__name__, template_folder="templates", static_folder="static")
# 为 jinja 注入 assets 对象
app.jinja_env.globals["assets"] = Assets(app)

# 获取 ENV 环境变量
env = os.environ.get("ENV")
# 根据 ENV 环境变量加载不同的配置文件
if env:
    app.config.from_pyfile(f"conf_{env}.py")
else:
    app.config.from_pyfile("conf.py")

# Controller 函数


@app.route("/", methods=["GET"])
@templated()
def index():
    return app.config


# 启动 Flask 应用
if __name__ == "__main__":
    # 启动 flask 应用
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        extra_files=watch_files_for_develop(app),
    )
