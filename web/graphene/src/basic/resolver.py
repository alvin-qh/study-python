"""解析器

对于 Graphene 框架来说, 一个字段的值有两种获取方式:

- 上一级解析器解析的对象中包含该字段;
- 当前字段所在的实体类型中提供了对应的 resolve 方法;

例如, 对于如下查询:

```graphql
query {
    foo {
        name
        value
    }
}
```

可以通过如下的 Python 代码来支持:

```python
class Query(ObjectType):
    foo = Field(Foo, required=True)

    def resolve_foo(parent: Literal[None], info: ResolveInfo) -> Foo:
        return Foo(name="foo")


class Foo(ObjectType):
    name = String(required=True)
    value = Int(required=True)

    def resolve_value(parent: "Foo", info: ResolveInfo) -> int:
        return len(parent.name)
```

在 `Query` 类型中, `foo` 字段 `resolve_foo` 方法返回了包含 `name` 字段的 `Foo` 类型对象, 所以
查询中的 `name` 字段得到满足, `value` 字段则是通过 `Foo` 类型的 `resolve_foo` 方法进行对应
"""

from collections import namedtuple
from typing import Literal, Union

from graphene import Field, ObjectType, ResolveInfo, Schema, String

# 定义中文名人员类型, xing 字段表示为姓, ming 字段表示名
ChinesePerson = namedtuple("ChinesePerson", ["xing", "ming"])


def get_chinese_person() -> ChinesePerson:
    """获取一个中文名的 `ChinesePerson` 对象

    Returns:
        ChinesePerson: `ChinesePerson` 对象, 具备 `xing`, `ming` 两个属性
    """
    return ChinesePerson("Qu", "Hao")


class Person(ObjectType):
    """人员类型

    对应的 GraphQL 定义如下:

    ```
    type Person {
        firstName
        lastName
        fullName
    }
    ```
    """

    first_name = String()
    last_name = String()
    full_name = String()

    @staticmethod
    def resolve_full_name(
        parent: Union[ChinesePerson, "Person"], info: ResolveInfo
    ) -> str:
        """解析 `full_name` 字段

        Args:
            parent (Union[ChinesePerson, Person]): 根据上一级解析, 可以是 `ChinesePerson` 和
            `Person` 任意类型

        Returns:
            str: 人员全名字段的值
        """
        # 判断 parent 参数类型
        if isinstance(parent, ChinesePerson):
            # 返回全名通过 xing 和 ming 两个字段组合
            return f"{parent.xing} {parent.ming}"

        # 返回全名通过 first_name 和 last_name 两个字段组合
        return f"{parent.first_name}·{parent.last_name}"


def resolve_person(
    parent: Literal[None],
    info: ResolveInfo,
    type: str,
) -> Union[Person, ChinesePerson]:
    """解析 `person` 字段, Graphene 可以使用独立的函数用作字段解析, 只需要在字段声明时指定 `resolver` 参数即可

    根据 `type` 参数的值, 该方法会返回 `ChinesePerson` 和 `Person` 类型的对象

    由于 `person` 字段的类型是 `Person`, 所以下一级解析会执行 `Person` 类型的 `resolve_full_name`
    方法, 但由于 `resolve_person` 返回的类型不同, 所以 `resolve_full_name` 方法的 `parent` 参数
    类型会可能是 `ChinesePerson` 或 `Person` 类型

    Args:
        type (str): 表示类型, 可以为 `"chinese"` 或其它字符串

    Returns:
        Union[ChinesePerson, Person]: 返回 `person` 字段可以同时为 `ChinesePerson`
        和 `Person` 类型
    """
    # 根据参数, 为 person 字段返回不同的类型
    if type == "chinese":
        # 返回 ChinesePerson 类型对象
        return get_chinese_person()

    # 返回 Person 类型对象
    return Person(
        first_name="Alvin",
        last_name="Qu",
    )


class Query(ObjectType):
    """定义 `Query` 类型

    对应的 GraphQL 定义如下:

    ```
    type Person {
        person(type: String = ""): Person!
    }
    ```
    """

    person = Field(
        Person, type=String(default_value=""), required=True, resolver=resolve_person
    )


"""定义 schema 对象, 对应的 GraphQL 定义为

```
schema {
    query: Query
}
```
"""
schema = Schema(query=Query)
