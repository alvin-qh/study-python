from typing import Any, Dict

from flask import Blueprint

from utils import templated

# 创建名为 home 的节点对象
bp = Blueprint("home", __name__)


@bp.route("/", methods=["GET"])
@templated()
def index() -> Dict[str, Any]:
    return {}
