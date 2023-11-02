from typing import Literal

from graphene import ResolveInfo
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType

from graphql import GraphQLError

from .models import Department as DepartmentModel
from .models import Employee as EmployeeModel
from .models import Role as RoleModel


class QueryError(GraphQLError):
    def __init__(self, message: str) -> None:
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
    def resolve_gender(
        parent: EmployeeModel, info: ResolveInfo
    ) -> Literal["male", "female"]:
        return parent.gender.value
