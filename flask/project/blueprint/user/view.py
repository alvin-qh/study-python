from typing import Any, Dict

from flask import Blueprint, request

from utils import templated

# 创建名为 user 的节点对象
bp = Blueprint("user", __name__)


@bp.route("/", methods=["GET"])
@templated()
def index() -> Dict[str, Any]:
    return dict(user={"name": request.args.get("name") or ""})
