from graphene import Schema

from .mutations import DepartmentMutation, EmployeeMutation
from .queries import DepartmentQuery, EmployeeQuery


class RootQuery(
    DepartmentQuery,
    EmployeeQuery,
):
    """定义根查询 Schema

    从 `DepartmentQuery` 和 `EmployeeQuery` 查询类继承, 包括父类的所有字段
    """


class RootMutation(
    DepartmentMutation,
    EmployeeMutation,
):
    """定义根变更 Schema

    从 `DepartmentMutation` 和 `EmployeeMutation` 查询类继承, 包括父类的所有字段
    """


# 创建 schema 对象
schema = Schema(
    query=RootQuery,
    mutation=RootMutation,
)
