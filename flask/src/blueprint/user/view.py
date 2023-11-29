from typing import Any, Dict

from utils import templated

from flask import Blueprint, request

# 创建名为 user 的节点对象
bp = Blueprint("user", __name__)


@bp.route("", methods=["GET"])
@templated("user.html")
def index() -> Dict[str, Any]:
    return dict(user={"name": request.args.get("name") or ""})
