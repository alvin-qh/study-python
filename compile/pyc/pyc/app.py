import time
from typing import Any, Dict, Literal, Tuple

from pyc.utils import templated

from flask import Flask, Response, jsonify

app = Flask(__name__, static_folder="static", template_folder="templates")


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
""",
        200,
    )


@app.route("/template", methods=["GET"])
@templated()
def template() -> Dict[str, Any]:
    return {"data": {"title": "Hello", "message": "Hello World"}}


@app.route("/json", methods=["GET"])
def use_json() -> Tuple[Response, Literal[200]]:
    tm = time.mktime(time.localtime(time.time()))
    return jsonify(time=int(tm)), 200
