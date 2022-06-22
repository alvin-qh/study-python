from typing import Literal

from graphene import (ID, Field, Interface, List, ObjectType, ResolveInfo,
                      Schema, String)


class Person(Interface):
    """
    定义一个接口类型, 该类型可作为所有实体类型 (`ObjectType`) 的接口类型

    对应的 GraphQL 定义如下:

    ```
    interface Person {
        id: ID!
        name: String!
        friends: [Person]!
    }
    ```
    """
    id = ID(required=True)
    name = String(required=True)
    friends = List(lambda: Person)


class Student(ObjectType):
    """
    定义实体类型, 实现了 `Person` 接口 (通过在 `Meta` 类型中指定接口类型)

    对应的 GraphQL 定义如下:

    ```
    type Student implements Person {
        classRoom: String!
    }
    ```
    """

    class Meta:
        """
        定义实体类型元类型

        本例中在元类型中, 通过 `interfaces` 字段指定了当前实体类型的接口类型.
        当前实体类型会继承接口类型中定义的字段和字段解析方法
        """
        # 指定当前实体类型的接口类型
        interfaces = (Person,)

    # 在接口定义的基础上增加新的实体字段
    class_room = String(required=True)


class Query(ObjectType):
    """
    定义根查询类型

    对应的 GraphQL 定义如下:

    ```
    type Query {
        classLeader: Student!
    }
    ```
    """
    # 定义要查询的字段, 为 Student 类型
    class_leader = Field(Student, required=True)

    @staticmethod
    def resolve_class_leader(parent: Literal[None], info: ResolveInfo) -> Student:
        """
        解析 `class_leader` 字段, 返回 `Student` 类型的实体对象

        Returns:
            Student: 获取一个 `Student` 类型的实体对象
        """
        # 定义 friend 字段值
        friend = Student(id=3, name="Lucy", class_room="2-1")
        # 定义 Student 实体对象并返回
        return Student(id=1, name="Alvin", friends=[friend], class_room="1-1")


"""
定义 schema 结构, 包括查询对象和定义的类型

对应的 GraphQL 定义为

```
schema {
    query: Query
}
```
"""
schema = Schema(query=Query, types=[Student])
