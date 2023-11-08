from graphene import Schema

from .mutations import DepartmentMutation, EmployeeMutation
from .queries import DepartmentQuery, EmployeeQuery


class RootQuery(
    DepartmentQuery,
    EmployeeQuery,
):
    """定义根查询 Schema"""

    pass


class RootMutation(
    DepartmentMutation,
    EmployeeMutation,
):
    """定义根变更 Schema"""

    pass


# 创建 schema 对象
schema = Schema(
    query=RootQuery,
    mutation=RootMutation,
)
