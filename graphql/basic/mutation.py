from typing import Any

from graphene import (InputObjectType, Int, Mutation, ObjectType, ResolveInfo,
                      Schema, String)


class Person(ObjectType):
    name = String(required=True)
    age = Int(required=True)


class CreatePerson1(Mutation):
    class Arguments:
        name = String(required=True)
        age = String(required=True)

    Output = Person

    @staticmethod
    def mutate(parent: Any, info: ResolveInfo, name: str, age: int) -> Person:
        return Person(name=name, age=age)


class PersonInput(InputObjectType):
    name = String(required=True)
    age = Int(required=True)


class CreatePerson2(Mutation):
    class Arguments:
        person_data = PersonInput(required=True)

    Output = Person

    @staticmethod
    def mutate(parent: Any, info: ResolveInfo, person_data: PersonInput) -> Person:
        return Person(name=person_data.name, age=person_data.age)


class Mutations(ObjectType):
    create_person1 = CreatePerson1.Field()
    create_person2 = CreatePerson2.Field()


class Query(ObjectType):
    answer = String(default_value="")


schema = Schema(query=Query, mutation=Mutations)
