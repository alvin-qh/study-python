from graphene import ResolveInfo, ObjectType
from graphene.relay import Node
from graphql import GraphQLError

from .models import (
    Department as DepartmentModel,
    Role as RoleModel,
    Employee as EmployeeModel
)


class QueryError(GraphQLError):
    def __init__(self, message: str):
        super().__init__(message)


class Department(ObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (Node,)


class Role(ObjectType):
    class Meta:
        model = RoleModel
        interfaces = (Node,)


class Employee(ObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (Node,)

    @staticmethod
    def resolve_gender(parent: EmployeeModel, info: ResolveInfo):
        return parent.gender.value
