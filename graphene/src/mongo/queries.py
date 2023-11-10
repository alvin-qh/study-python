from typing import Any
from typing import List as ListType
from typing import Literal, cast

from graphene import ConnectionField, Field, ObjectType, ResolveInfo, String

from .models import Department as DepartmentModel
from .models import Employee as EmployeeModel
from .types import BaseConnection, Department, Employee, QueryError, QueryResult
from .utils import parse_cursor


class DepartmentQuery(ObjectType):
    """部门查询类"""

    # 表示要查询 `Department` 类型结果
    department: Department = Field(
        Department,
        args={
            "name": String(required=True),  # 定义查询参数, 表示部门名称
        },
    )

    @staticmethod
    def resolve_department(
        parent: Literal[None], info: ResolveInfo, name: str
    ) -> DepartmentModel:
        """解析 `department` 字段, 表示输出查询结果

        Args:
            - `name` (`str`): 查询参数, 表示部门名称

        Returns:
            `DepartmentModel`: 查询结果, 表示部门实体对象
        """
        return cast(DepartmentModel, DepartmentModel.objects(name=name).first())


class EmployeeConnection(BaseConnection[Employee]):
    """员工批量查询类型"""

    class Meta:
        """`Connection` 类型的元数据类, 设定 node 的类型"""

        node = Employee


class EmployeeQuery(ObjectType):
    """员工查询类型"""

    # 表示要查询 `Employee` 类型结果
    employee: Employee = Field(
        Employee,
        args={
            "name": String(required=True),  # 定义查询参数, 表示员工姓名
        },
    )

    # 表示要查询 `Employee` 集合结果, 即通过部门名称查询一个部门下的所有员工
    employees: ListType[Employee] = ConnectionField(
        EmployeeConnection,
        args={
            "department_name": String(required=True),  # 定义查询参数, 表示部门名称
        },
    )

    @staticmethod
    def resolve_employee(
        parent: Literal[None], info: ResolveInfo, name: str
    ) -> EmployeeModel:
        """解析 `employee` 字段, 表示根据员工姓名查询员工对象

        Args:
            - `name` (`str`): 查询参数, 表示员工姓名

        Returns:
            `EmployeeModel`: 查询结果, 为员工实体对象
        """
        return cast(EmployeeModel, EmployeeModel.objects(name=name).first())

    @staticmethod
    def resolve_employees(
        parent: Literal[None], info: ResolveInfo, department_name: str, **kwargs: Any
    ) -> EmployeeConnection:
        """解析 `employees` 字段, 表示根据部门名称查询部门下所有员工集合

        Args:
            - `department_name` (`str`): 查询参数, 表示部门名称
            - `kwargs` (`Dict[str, Any]`): 其它查询参数, 包括分页参数

        Raises:
            `QueryError`: 查询错误异常

        Returns:
            `EmployeeConnection`: 查询结果, 表示部门下员工对象的集合
        """
        # 根据 `first` 查询参数计算分页大小
        page_size: int = max(cast(int, kwargs.get("first", 0)), 0)
        if page_size == 0:
            raise QueryError("invalid_first_argument")

        # 根据 `after` 查询参数计算分页开始位置
        after: str = kwargs.get("after", "")
        if after:
            # 将游标解析为数值
            start = int(parse_cursor(after))
        else:
            start = 0

        # 根据部门名称查询部门实体对象
        department: Department = DepartmentModel.objects(name=department_name).first()

        # 计算部门下所有员工的数量
        total_count: int = EmployeeModel.objects(department=department).count()

        # 根据分页查询部门下员工集合
        employees: ListType[EmployeeModel] = list(
            EmployeeModel.objects(department=department).limit(page_size).skip(start)
        )

        # 计算查询结果实际分页大小
        page_size = len(employees)

        # 包装查询结果供 EmployeeConnection 类型解析
        result = QueryResult(
            employees,
            start,
            start + page_size,
            total_count,
        )

        return EmployeeConnection(result)
