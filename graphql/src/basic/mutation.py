"""
更新操作

若要对实体对象进行更新操作 (添加/修改/删除), 需要用到 `Mutation` 类型.

```graphql
type Mutation {
    createFoo(name: String!): FooCreatedPayload!
    updateFoo(fooData: FooInput): FooUpdatedPayload!
    deleteFoo(id: ID!): FooDeletedPayload!
}
```

其中的 `FooInput` 是一个输入类型, 用作输入参数, 定义如下:

```graphql
input FooInput {
    id: ID!
    name: String!
}
```

其中的 `FooCreatedPayload`, `FooUpdatedPayload` 和 `FooDeletedPayload` 是实体类型, 表示返回值, 例如:

```graphql
type FooCreatedPayload {
    createdFoo: Foo!
}
```

通过 Graphene 定义 Mutation 操作如下:

```python
class CreateFoo(Mutation):
    class Argument:
        name = String(required=True)

    Output = FooCreatedPayload

    @staticmethod
    def mutate(parent: Literal[None], info: ResolveInfo, name: str) -> FooCreatedPayload:
        foo = Foo(name=name)
        # persistent foo object
        return FooCreatedPayload(createdFoo=foo)
```

字段 `Output` 表示操作完成后返回的类型

使用 Graphene 定义 Input 类型如下:

```python
class FooInput(InputObjectType):
    id = ID(required=True)
    name = String(required=True)
```

该 Input 类型可以作为 Mutation 类型的参数, 例如:

```python
class UpdateFoo(Mutation):
    class Argument:
        foo_data = FooInput(required=True)

    Output = FooUpdatedPayload

    @staticmethod
    def mutate(parent: Literal[None], info: ResolveInfo, foo_data: FooInput) -> FooUpdatedPayload:
        foo = Foo.find(int(foo_data.id))
        if not foo:
            return FooCreatedPayload(updatedFoo=None)

        foo.name = foo_data.name
        return FooUpdatedPayload(createdFoo=foo)
```

最后, 定义 `Mutations` 类型为:

```python
class Mutations(ObjectType):   # Mutation 名称已被 Graphene 内置类型占用
    createFoo = CreateFoo.Field()
    updateFoo = UpdateFoo.Field()
    deleteFoo = DeleteFoo.Field()
```

在创建 `Schema` 对象时, 将 `Mutations` 对象作为参数传入即可
"""

from typing import Literal

from graphene import (
    InputObjectType,
    Int,
    Mutation,
    ObjectType,
    ResolveInfo,
    Schema,
    String,
)


class Person(ObjectType):
    """
    实体类

    ```graphql
    type Person {
        name: String!
        age: Int!
    }
    ```
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
    def mutate(
        parent: Literal[None], info: ResolveInfo, person_data: PersonInput
    ) -> Person:
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


"""
定义 schema 结构

对应的 GraphQL 定义为

```graphql
schema {
    query: Query
    mutation: Mutations
}
```
"""
schema = Schema(query=Query, mutation=Mutations)
