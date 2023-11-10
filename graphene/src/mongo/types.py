from typing import Any, Generic
from typing import List as ListType
from typing import Literal, Optional, TypeVar, cast

from graphql import GraphQLError

from graphene import (
    Connection,
    Enum,
    Field,
    Int,
    ObjectType,
    PageInfo,
    ResolveInfo,
    String,
)

from .dataloaders import department_loader, employee_loader, role_loader
from .models import Department as DepartmentModel
from .models import Employee as EmployeeModel
from .models import Gender as GenderModel
from .models import Role as RoleModel
from .utils import make_cursor


class QueryError(GraphQLError):
    """定义表示查询异常的 Graphql 错误对象"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class Department(ObjectType):
    """定义部门 Graphql 类型"""

    # 部门 id 字段
    id: str = String(required=True)

    # 部门名称字段
    name: str = String(required=True)

    # 部门级别字段
    level: int = Int(required=True, default_value=0)

    # 部门主管字段, 表示一个 `Employee` 类型对象
    manager: Optional[EmployeeModel] = Field(lambda: Employee, required=False)

    @staticmethod
    async def resolve_manager(
        parent: DepartmentModel, info: ResolveInfo
    ) -> Optional[EmployeeModel]:
        """解析部门主管字段"""
        if not parent.manager:
            return None

        manager = await employee_loader.load(str(parent.manager.id))
        return manager


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
    gender: GenderModel = Field(Gender, required=True, default_value=GenderModel.male)

    # 员工所属部门
    department: Optional[DepartmentModel] = Field(Department, required=False)

    # 员工角色
    role: Optional[Role] = Field(Role, required=True)

    @staticmethod
    def resolve_gender(
        parent: EmployeeModel, info: ResolveInfo
    ) -> Literal["male", "female"]:
        """解析员工性别字段"""
        return parent.gender.value

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


T = TypeVar("T")


class QueryResult(PageInfo, Generic[T]):
    """保存查询结果的类型, 记录一页的数据以及分页信息"""

    # 为继承 `Generic` 类打的补丁
    __parameters__ = ("~T",)

    def __init__(self, data: ListType[T], start: int, end: int, count: int) -> None:
        self._data = data
        self.start = start
        self.end = end
        self.count = count

    @property
    def start_cursor(self) -> str:
        """获取起始游标值

        Returns:
            int: 游标值
        """
        return make_cursor(self.start)

    @property
    def end_cursor(self) -> str:
        """获取终止游标值

        Returns:
            int: 游标值
        """
        return make_cursor(self.end)

    @property
    def has_next_page(self) -> bool:
        """是否有下一页

        Returns:
            bool: 是否有下一页
        """
        return self.end < self.count

    @property
    def has_previous_page(self) -> bool:
        """是否有上一页

        Returns:
            bool: 是否有上一页
        """
        return self.start > 0

    @property
    def data(self) -> ListType[T]:
        """获取一页的数据

        Returns:
            ListType[T]: 一页数据的集合
        """
        return self._data


class BaseConnection(Connection, Generic[T]):
    """连接类型超类"""

    # 为继承 `Generic` 类打的补丁
    __parameters__ = ("~T",)

    class Meta:
        abstract = True

    class Edge:
        """设置 `Connection` 中的元素"""

        def __init__(self, **kwargs: Any) -> None:
            """占位方法, 不会被调用"""

    # 表示全部数据数量的属性
    total_count = Int()

    def resolve_total_count(self, info: ResolveInfo) -> int:
        """解析总记录数属性

        Args:
            info (ResolveInfo): 解析上下文对象

        Returns:
            int: 总记录数
        """
        return cast(QueryResult[Any], self.page_info).count

    def resolve_edges(self, info: ResolveInfo) -> ListType[Edge]:
        """解析 `edges` 属性

        Args:
            info (ResolveInfo): 解析上下文对象

        Returns:
            ListType[Edge]: Edge 对象集合
        """
        start = self.page_info.start
        return [
            self.Edge(cursor=start + n, node=data)
            for n, data in enumerate(self.page_info.data)
        ]
