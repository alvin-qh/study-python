from typing import Any, Generic
from typing import List as ListType
from typing import Literal, Optional, TypeVar, cast

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

from graphql import GraphQLError

from .dataloaders import department_loader, employee_loader, role_loader
from .models import Department as DepartmentModel
from .models import Employee as EmployeeModel
from .models import Gender as GenderModel
from .models import Role as RoleModel
from .utils import make_cursor


class QueryError(GraphQLError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class Department(ObjectType):
    id: str = String(required=True)
    name: str = String(required=True)
    level: int = Int(required=True, default_value=0)
    manager: Optional[EmployeeModel] = Field(lambda: Employee, required=False)

    @staticmethod
    async def resolve_manager(
        parent: DepartmentModel, info: ResolveInfo
    ) -> Optional[EmployeeModel]:
        if not parent.manager:
            return None

        manager = await employee_loader.load(str(parent.manager.id))
        return manager


class Role(ObjectType):
    id: str = String(required=True)
    name: str = String(required=True)


Gender = Enum.from_enum(GenderModel)


class Employee(ObjectType):
    id: str = String(required=True)
    name: str = String(required=True)
    gender: GenderModel = Field(Gender, required=True, default_value=GenderModel.male)
    department: Optional[DepartmentModel] = Field(Department, required=False)
    role: Optional[Role] = Field(Role, required=True)

    @staticmethod
    def resolve_gender(
        parent: EmployeeModel, info: ResolveInfo
    ) -> Literal["male", "female"]:
        return parent.gender.value

    @staticmethod
    async def resolve_department(
        parent: EmployeeModel, info: ResolveInfo
    ) -> Optional[DepartmentModel]:
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
