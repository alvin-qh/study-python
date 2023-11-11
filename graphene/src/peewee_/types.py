from typing import Any
from typing import List as ListType
from typing import Optional, cast

from graphql import GraphQLError
from peewee import ModelSelect

from graphene import ConnectionField, Enum, Field, Int, ObjectType, ResolveInfo, String

from .core import BaseConnection, QueryResult, parse_cursor
from .dataloaders import department_loader, employee_loader, role_loader
from .models import Department as DepartmentModel
from .models import Employee as EmployeeModel
from .models import Gender as GenderModel
from .models import Role as RoleModel


class QueryError(GraphQLError):
    """定义表示查询异常的 Graphql 错误对象"""

    def __init__(self, message: str):
        super().__init__(message)


class Role(ObjectType):
    """定义权限 Graphql 类型"""

    # 权限 id
    id: str = String(required=True)

    # 权限名称
    name: str = String(required=True)


# 将 Python 枚举转为 Graphql 枚举类型
Gender = Enum.from_enum(GenderModel)


class Employee(ObjectType):
    """定义员工 Graphql 类型"""

    # 员工 id
    id: str = String(required=True)

    # 员工姓名
    name: str = String(required=True)

    # 员工性别
    gender: GenderModel = Field(Gender, required=True, default_value=GenderModel.MALE)

    # 员工所属部门
    department: Optional[DepartmentModel] = Field(lambda: Department, required=False)

    # 员工角色
    role: Optional[Role] = Field(Role, required=True)

    @staticmethod
    def resolve_gender(parent: EmployeeModel, info: ResolveInfo) -> GenderModel:
        """解析员工性别字段"""
        return GenderModel(parent.gender)

    @staticmethod
    async def resolve_department(
        parent: EmployeeModel, info: ResolveInfo
    ) -> Optional[DepartmentModel]:
        """解析员工所属部门字段"""
        if not parent.department:
            return None

        department: DepartmentModel = await department_loader.load(
            str(parent.department.id)
        )
        return department

    @staticmethod
    async def resolve_role(
        parent: EmployeeModel, info: ResolveInfo
    ) -> Optional[RoleModel]:
        """解析员工角色字段"""
        if not parent.role:
            return None

        role: RoleModel = await role_loader.load(str(parent.role.id))
        return role


class EmployeeConnection(BaseConnection[Employee]):
    """员工批量查询类型"""

    class Meta:
        """`Connection` 类型的元数据类, 设定 node 的类型"""

        node = Employee


class Department(ObjectType):
    """定义部门 Graphql 类型"""

    # 部门 id 字段
    id: str = String(required=True)

    # 部门名称字段
    name: str = String(required=True)

    # 部门级别字段
    level: int = Int(required=True, default_value=0)

    # 部门主管字段, 表示一个 `Employee` 类型对象
    manager: Optional[EmployeeModel] = Field(Employee, required=False)

    # 表示要查询 `Employee` 集合结果, 即当前部门下的所有员工
    employees: EmployeeConnection = ConnectionField(
        EmployeeConnection,
        args={
            "gender": String(),  # 定义查询参数, 表示员工性别
        },
    )

    @staticmethod
    async def resolve_manager(
        parent: DepartmentModel, info: ResolveInfo
    ) -> Optional[EmployeeModel]:
        """解析部门主管字段"""
        if not parent.manager:
            return None

        manager = await employee_loader.load(str(parent.manager.id))
        return manager

    @staticmethod
    def resolve_employees(
        parent: DepartmentModel, info: ResolveInfo, gender: Optional[str], **kwargs: Any
    ) -> EmployeeConnection:
        """解析 `employees` 字段, 表示当前部门下的所有员工

        Args:
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

        page_num = (start // 10) + 1

        query: ModelSelect = EmployeeModel.select().where(
            EmployeeModel.department == parent
        )
        if gender:
            query = query.where(EmployeeModel.gender == GenderModel[gender].value)

        # 计算部门下所有员工的数量
        total_count: int = query.count()

        # 根据分页查询部门下员工集合
        employees: ListType[EmployeeModel] = list(query.paginate(page_num, page_size))

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
