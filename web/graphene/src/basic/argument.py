"""演示如何在 Graphql 查询中传递参数

在 Graphql 结构中, 可以定义参数和传递参数, 例如如下定义:

```graphql
type Query {
    user(id: ID!): User!
}
```

上述结构定义了一个具备 `user` 字段的查询类型, 查询 `user` 字段需要传递 `id` 参数, 例如如下查询结构:

```graphql
query ($id: ID!) {  # 定义名为 $id 的形参, Scalar 类型为 ID
    user(id: $id) { # 指定查询 `user` 字段时需要传递的实参, 即将 $id 参数值传递给 id 参数
        id
        name
        birthday
    }
}
```

执行上述查询结构时, 需要指定查询参数, 即给形参 `$id` 传参, 例如: `{"id": 100}`

通过 Graphene 框架, 有如下几种形式可以定义参数, 包括:-

- 通过 `Field` 类型的 `**extra_args` 参数传递任意 `Scalar` 类型命名参数:
    `user = Field(User, name=String(required=True))`, 定义 `name` 参数且规定必须传递

- 通过 `Field` 类型的 `**extra_args` 参数传递任意 `Argument` 类型命名参数
    `user = Field(User, name=Argument(String, required=True))`, 定义 `name` 参数且规定必须传递

- 当定义的参数名和 `Field` 类型构造器参数冲突 (例如: `required` 参数), 则可以通过 `Field` 类型的 `args` 参数设置
    `user = Field(User, args={"name": String(required=True)})`

在定义字段解析方法时, 所有定义在字段上的参数均会成为方法参数

```python
def resolve_user(parent: Literal[None], info: ResolveInfo, name: str) -> User:
    ...
```

或者一次性接收所有参数

```python
def resolve_user(parent: Literal[None], info: ResolveInfo, **kwargs) -> User:
    name = kwargs["name"]
    ...
```
"""

from typing import Any, Literal

from graphene import Argument, Field, ObjectType, ResolveInfo, Schema, String


class Human(ObjectType):
    """实体类型, 表示一个人类类型

    对应的 GraphQL 定义为:

    ```
    type Human {
        firstName: String
        lastName: String
    }
    ```
    """

    # 首名称
    first_name = String(default_value="")

    # 末名称
    last_name = String(default_value="")

    @staticmethod
    def get_human(name: str) -> "Human":
        """根据一个全名获取 `Human` 实体对象

        Args:
            name (str): 全名, 用 `·` 分隔

        Returns:
            Human: 返回实体对象
        """
        first_name, last_name = name.split("·", 1)
        return Human(first_name=first_name, last_name=last_name)


class Query(ObjectType):
    """查询对象, 演示查询时的参数传递

    对应的 GraphQL 定义为:

    ```
    type Query {
        human1(name: String!): Human!
        human2(name: String!): Human!
        human3(name: String!): Human!
    }
    ```
    """

    # 第一种声明参数的方式, 通过 **extra_args 参数, 将 Scalar 对象作为查询参数
    human1 = Field(Human, required=True, name=String(required=True))

    # 第二种声明参数的方式, 通过 **extra_args 参数, 将Argument 对象作为参数, Scalar 类型作为参数类型
    human2 = Field(Human, required=True, name=Argument(String, required=True))

    # 第三种声明参数的方式, 通过 args 参数和一个 Dict 对象作为参数列表
    # 这种方式比较繁琐, 一般用于参数名和 Field 构造器参数冲突 (例如 required) 时使用
    human3 = Field(Human, required=True, args={"name": String(required=True)})

    @staticmethod
    def resolve_human1(parent: Literal[None], info: ResolveInfo, name: str) -> Human:
        """解析字段, 通过命名参数接收查询参数 (`name` 参数), 该参数是通过 `Field` 类型构造器的 `**extra_args`
        参数传递的

        Args:
            name (str): 接收 `name` 查询参数

        Returns:
            Human: 查询到的 `Human` 实体对象
        """
        return Human.get_human(name=name)

    @staticmethod
    def resolve_human2(
        parent: Literal[None], info: ResolveInfo, **kwargs: Any
    ) -> Human:
        """解析字段, 通过命名参数接收查询参数 (`name` 参数), 该参数是通过 `Field` 类型构造器的 `**extra_args`
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
        """解析字段, 通过命名参数接收查询参数 (`name` 参数), 该参数是通过 `Field` 类型构造器的 `args`
        参数传递的

        Args:
            name (str): 接收 `name` 查询参数

        Returns:
            Human: 查询到的 `Human` 实体对象
        """
        return Human.get_human(name=name)


"""定义 schema 对象

对应的 GraphQL 定义为

```
schema {
    query: Query
}
```
"""
schema = Schema(query=Query)
