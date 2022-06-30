from typing import Literal

from graphene import Argument, Field, ObjectType, ResolveInfo, Schema, String


class Human(ObjectType):
    """
    实体类型, 表示一个人类类型
    """
    # 首名称
    first_name = String(default_value="")

    # 末名称
    last_name = String(default_value="")

    @staticmethod
    def get_human(name: str) -> "Human":
        """
        根据一个全名获取 `Human` 实体对象

        Args:
            name (str): 全名, 用 `·` 分隔

        Returns:
            Human: 返回实体对象
        """
        first_name, last_name = name.split("·", 1)
        return Human(first_name=first_name, last_name=last_name)


class Query(ObjectType):
    """
    查询对象, 演示查询时的参数传递
    """
    # 第一种声明参数的方式, 通过 **extra_args 参数, 将 Scalar 对象作为查询参数
    human1 = Field(Human, required=True, name=String(required=True))

    # 第二种声明参数的方式, 通过 **extra_args 参数, 将Argument 对象作为参数, Scalar 类型作为参数类型
    human2 = Field(Human, required=True, name=Argument(String, required=True))

    # 第三种声明参数的方式, 通过 args 参数和一个 Dict 对象作为参数列表
    # 这种方式比较繁琐, 一般用于参数名和 Field 构造器参数冲突 (例如 required) 时使用
    human3 = Field(Human, required=True, args={
        "name": String(required=True)
    })

    @staticmethod
    def resolve_human1(parent: Literal[None], info: ResolveInfo, name: str) -> Human:
        """
        解析字段, 通过命名参数接收查询参数 (`name` 参数), 该参数是通过 `Field` 类型构造器的 `**extra_args`
        参数传递的

        Args:
            name (str): 接收 `name` 查询参数

        Returns:
            Human: 查询到的 `Human` 实体对象
        """
        return Human.get_human(name=name)

    @staticmethod
    def resolve_human2(parent: Literal[None], info: ResolveInfo, **kwargs) -> Human:
        """
        解析字段, 通过命名参数接收查询参数 (`name` 参数), 该参数是通过 `Field` 类型构造器的 `**extra_args`
        参数传递的

        Args:
            name (str): 接收 `name` 查询参数

        Returns:
            Human: 查询到的 `Human` 实体对象
        """
        if "name" not in kwargs:
            return Human(first_name="", last_name="")

        return Human.get_human(name=kwargs["name"])

    @staticmethod
    def resolve_human3(parent: Literal[None], info: ResolveInfo, name: str) -> Human:
        """
        解析字段, 通过命名参数接收查询参数 (`name` 参数), 该参数是通过 `Field` 类型构造器的 `args`
        参数传递的

        Args:
            name (str): 接收 `name` 查询参数

        Returns:
            Human: 查询到的 `Human` 实体对象
        """
        return Human.get_human(name=name)


schema = Schema(query=Query)
