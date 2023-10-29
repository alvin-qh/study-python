from graphene import Schema

from .mutations import (
    Mutations
)
from .queries import (
    DepartmentQuery,
    EmployeeQuery
)


class RootQuery(
    DepartmentQuery,
    EmployeeQuery
):
    pass


class RootMutation(
    Mutations
):
    pass


# noinspection PyTypeChecker
schema = Schema(query=RootQuery, mutation=RootMutation)
