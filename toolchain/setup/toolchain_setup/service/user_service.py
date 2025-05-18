import json
from os import path
from toolchain_setup.model import User

# 获取当前文件路径
CUR_DIR = path.abspath(path.dirname(__file__))


def load_users() -> list[User]:
    """从 `conf/conf.json` 文件中读取用户信息

    Returns:
        list[User]: 返回用户对象集合
    """
    with open(path.join(CUR_DIR, "../conf/conf.json")) as f:
        data = json.load(f)
        return [User(**user) for user in data["users"]]
