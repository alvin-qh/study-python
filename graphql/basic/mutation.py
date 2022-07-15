from typing import Any, Literal
from unicodedata import name

from graphene import (InputObjectType, Int, Mutation, ObjectType, ResolveInfo,
                      Schema, String)


class Person(ObjectType):
    """
    实体类

    type Person {
        name: String!
        age: Int!
    }
    """
    # 姓名字段, 字符串类型
    name = String(required=True)
    # 年龄字段, 字符串类型
    age = Int(required=True)


class CreatePerson1(Mutation):
    """
    通过 `Scalar` 类型参数更像实体的 `Mutation` 类型
    """
    class Arguments:
        """
        `Mutation` 类型的参数类型
        """
        name = String(required=True)
        age = Int(required=True)

    # 完成更新操作后的返回类型
    Output = Person

    @staticmethod
    def mutate(parent: Literal[None], info: ResolveInfo, name: str, age: int) -> Person:
        """
        执行更像操作

        Args:
            name (str): 用户名
            age (int): 年龄

        Returns:
            Person: `Person` 类型实体对象
        """
        return Person(name=name, age=age)


class PersonInput(InputObjectType):
    """
    输入类, 用于输入要创建的对象

    对应的 Graphql 定义为

    ```graphql
    input PersonInput {
        name: String!
        age: Int!
    }
    ```
    """
    # 姓名字段
    name = String(required=True)
    # 年龄字段
    age = Int(required=True)

    def to_scalar(self) -> Person:
        """
        将当前对象转为 `Person` 类型的对象

        Returns:
            Person: `Person` 类型对象
        """
        return Person(
            name=self.name,
            age=self.age,
        )


class CreatePerson2(Mutation):
    """
    通过 `InputObjectType` 作为参数更像实体的 `Mutation` 类型
    """
    class Arguments:
        """
        执行更新操作的参数类型
        """
        # 通过 `InputObjectType` 类型作为参数字段
        person_data = PersonInput(required=True)

    # 执行更新后返回的结果类型
    Output = Person

    @staticmethod
    def mutate(parent: Literal[None], info: ResolveInfo, person_data: PersonInput) -> Person:
        """
        执行更像操作, 创建一个 `Person` 类型实体对象

        Args:
            person_data (PersonInput): `PersonInput` 类型参数对象

        Returns:
            Person: `Person` 类型实体对象
        """
        person = person_data.to_scalar()
        return person


class Mutations(ObjectType):
    """
    进行更新处理的实体类型

    对应的 Graphql 定义为:

    ```graphql
    type Mutations {
        createPerson1(name: String!, age: Int!): Person!
        createPerson2(personData: PersonInput!): Person!
    }
    ```
    """
    # 通过 scalar 类型参数执行更新的 Mutation 字段
    create_person1 = CreatePerson1.Field()

    # 通过 InputObjectType 类型参数执行更新的 Mutation 字段
    create_person2 = CreatePerson2.Field()


class Query(ObjectType):
    """
    创建查询实体类 (本测试中无用, 仅为填充参数)
    """
    # 定义一个任意字段
    answer = String(default_value="")


"""_summary_

"""
schema = Schema(query=Query, mutation=Mutations)
