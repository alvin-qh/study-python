from graphene import ResolveInfo
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from graphql import GraphQLError

from .models import (
    Department as DepartmentModel,
    Role as RoleModel,
    Employee as EmployeeModel
)


class QueryError(GraphQLError):
    def __init__(self, message: str):
        super().__init__(message)


class Department(MongoengineObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (Node,)


class Role(MongoengineObjectType):
    class Meta:
        model = RoleModel
        interfaces = (Node,)


class Employee(MongoengineObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (Node,)

    @staticmethod
    def resolve_gender(parent: EmployeeModel, info: ResolveInfo):
        return parent.gender.value
