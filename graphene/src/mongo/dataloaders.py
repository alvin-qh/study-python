from typing import Iterable
from typing import List as ListType

from aiodataloader import DataLoader

from .models import Department as DepartmentModel
from .models import Employee as EmployeeModel
from .models import Role as RoleModel


class DepartmentLoader(DataLoader[str, DepartmentModel]):
    """定义 `DepartmentModel` 类型的 Loader 类"""

    async def batch_load_fn(self, keys: Iterable[str]) -> ListType[DepartmentModel]:
        """批量读取部门数据

        Args:
            keys (Iterable[str]): Key 集合迭代器对象

        Returns:
            Promise[List[DepartmentModel]]: 异步对象, 可获取 `DepartmentModel` 实体类对象集合
        """
        return list(DepartmentModel.objects(id__in=keys))


# 实例化 Dataloader 对象
department_loader = DepartmentLoader()


class EmployeeLoader(DataLoader[str, EmployeeModel]):
    """定义 `EmployeeModel` 类型的 Loader 类"""

    async def batch_load_fn(self, keys: Iterable[str]) -> ListType[EmployeeModel]:
        """批量读取员工数据

        Args:
            keys (Iterable[str]): Key 集合迭代器对象

        Returns:
            Promise[List[EmployeeModel]]: 异步对象, 可获取 `EmployeeModel` 实体类对象集合
        """
        return list(EmployeeModel.objects(id__in=keys))


# 实例化 Dataloader 对象
employee_loader = EmployeeLoader()


class RoleLoader(DataLoader[str, RoleModel]):
    """定义 `RoleModel` 类型的 Loader 类"""

    async def batch_load_fn(self, keys: Iterable[str]) -> ListType[RoleModel]:
        """批量读取角色数据

        Args:
            keys (Iterable[str]): Key 集合迭代器对象

        Returns:
            Promise[List[RoleModel]]: 异步对象, 可获取 `RoleModel` 实体类对象集合
        """
        return list(RoleModel.objects(id__in=keys))


# 实例化 Dataloader 对象
role_loader = RoleLoader()
