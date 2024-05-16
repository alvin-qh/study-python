from datetime import date
from typing import Any, Dict, List, Optional, Set, TypedDict, Union, cast

from pymongo import MongoClient

# 定义文档类型
DocType = Dict[str, Any]

# 连接 mongodb
client: MongoClient[DocType] = MongoClient(
    host="127.0.0.1",  # 地址
    port=27017,  # 端口号
    directConnection=True,  # 对于单节点集群, 必须设置为 True
    # username="root",      # 对于集群, 在没有设置 Key 文件时, 无法设置用户名和密码
    # password="password",
    replicaset="rs0",  # 连接的集群名称
)

# 创建或切换到指定数据库
mongo_db = client.study_python_mongo


class CityModel(TypedDict):
    """定义表示城市的实体类型"""

    # 城市名称
    name: str

    # 国家名称
    country: str


class UserModel(TypedDict):
    """定义表示用户的实体类型"""

    # 用户名
    name: str

    # 用户生日
    birthday: Union[date, str]

    # 用户所在城市
    city: CityModel  # 关联到城市实体类型, 实际存储时, 存储关联到文档的 id


def clear_all() -> None:
    """删除所有的文档集合"""
    # 获取文档集名称列表
    collection_names = mongo_db.list_collection_names()
    for coll in collection_names:
        # 逐一删除文档集
        mongo_db.drop_collection(coll)


def create_user(user: UserModel) -> None:
    """创建一个用户实体文档

    Args:
        - `user` (`UserModel`): 用户实体对象
    """
    # 为用户的城市属性设置默认国家
    user["city"].setdefault("country", "China")

    # 将用户的生日转为字符串类型
    if user["birthday"] and isinstance(user["birthday"], date):
        user["birthday"] = user["birthday"].isoformat()

    # 启动 mongo 会话, 并设置 causal_consistency 以要求结果一致性
    with client.start_session(causal_consistency=True) as session:
        # 启动事务
        with session.start_transaction():
            # 查找指定的城市
            city = mongo_db.city.find_one(
                {"city": user["city"]["country"], "country": user["city"]["name"]},
                session=session,
            )

            # 城市不存在的情况下, 创建城市
            if not city:
                city = cast(DocType, user["city"])

                # 创建城市, 返回记录 id
                city["_id"] = mongo_db.city.insert_one(
                    city,
                    session=session,
                ).inserted_id

            # 在用户文档中设置城市文档的 id
            user["city"] = city["_id"]

            # 存储用户文档
            mongo_db.user.insert_one(cast(DocType, user), session=session)


def find_user(
    *,
    name: Optional[str] = None,
    birthday: Optional[Union[date, str]] = None,
    with_id: bool = False,
) -> List[UserModel]:
    """查询用户文档

    Args:
        - `name` (`Optional[str]`, optional): 要匹配的用户名称. Defaults to `None`.
        - `birthday` (`Optional[Union[date, str]]`, optional): 要匹配的用户生日. Defaults to `None`.
        - `with_id` (`bool`, optional): 查询结果中是否要包含 id 值. Defaults to `False`.

    Returns:
        `Optional[UserModel]`: 用户实体对象
    """
    # 存储结果的用户列表
    users: List[DocType] = []

    # 查询过滤器字典
    filter_: Dict[str, Any] = {}
    if name:
        filter_["name"] = name  # 设置姓名过滤条件

    if birthday:
        if isinstance(birthday, date):
            birthday = birthday.isoformat()

        filter_["birthday"] = birthday  # 设置生日过滤条件

    # 查询结果设置字典
    projection: Optional[Dict[str, Any]] = None
    if not with_id:
        projection = {"_id": False}  # 取消 _id 字段显式

    if len(filter_) > 0:
        # 查询符合条件的用户文档集合
        users = list(mongo_db.user.find(filter_, projection=projection))
        if not users:
            return []

        # 记录用户相关城市文档 id 的集合
        city_ids: Set[str] = set()
        for user in users:
            # 遍历用户文档集合

            # 将用户生日转为字符串
            if user["birthday"]:
                user["birthday"] = date.fromisoformat(user["birthday"])

            # 将用户相关城市文档 id 记录到集合中
            city_ids.add(user["city"])

        if city_ids:
            # 根据城市文档 id 集合查询城市文档集合
            cities = {
                c["_id"]: c
                for c in mongo_db.city.find({"_id": {"$in": list(city_ids)}})
            }

            # 遍历用户集合, 将城市文档进行关联
            for user in users:
                city = cities.get(user["city"])
                if city:
                    del city["_id"]
                    user["city"] = city

    # 返回用户实体集合
    return cast(List[UserModel], users)
