import time
from typing import Any, Dict, Literal, Tuple

from utils import templated, watch_files_for_develop

from flask import Flask, Response, jsonify

# 创建 Flask 对象，并指定静态文件存储路径以及 html 模板存储路径
app = Flask(__name__, static_folder="static", template_folder="templates")

# 定义 route


@app.route("/", methods=["GET"])
def index() -> Tuple[str, int]:
    return (
        """<!DOCTYPE html>
<html lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>Hello</title>
</head>
<body>
  <h1>Hello World</h1>
  <a href="/template">Next</a>
</body>
</html>
""", 200
    )


@app.route("/template", methods=["GET"])
@templated()
def template() -> Dict[str, Any]:
    return dict(data={"title": "Hello", "message": "Hello World"})


@app.route("/json", methods=["GET"])
def use_json() -> Tuple[Response, Literal[200]]:
    tm = time.mktime(time.localtime(time.time()))
    return jsonify(time=int(tm)), 200


# 进程启动时执行
if __name__ == "__main__":
    # 启动 flask 应用
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        extra_files=watch_files_for_develop(app),
    )
