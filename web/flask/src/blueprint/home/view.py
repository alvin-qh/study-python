from typing import Any, Dict

from utils.web import templated

from flask import Blueprint

# 创建名为 home 的节点对象
bp = Blueprint("home", __name__)


@bp.route("", methods=["GET"])
@templated("home.html")
def index() -> Dict[str, Any]:
    return {}
