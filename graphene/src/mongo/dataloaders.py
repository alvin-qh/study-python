from typing import Iterable
from typing import List
from typing import List as ListType
from typing import TypeVar

from aiodataloader import DataLoader
from mongoengine import Document

from .models import Department as DepartmentModel
from .models import Employee as EmployeeModel
from .models import Role as RoleModel

_DOC = TypeVar("_DOC", bound=Document)


def _order_by_keys(keys: Iterable[str], docs: Iterable[_DOC]) -> List[_DOC]:
    """将查询结果按照所给的 `keys` 的顺序进行排列

    Args:
        - `keys` (Iterable[str]): id 集合, 对应着 `docs` 参数集合中各个文档的 id 属性
        - `docs` (Iterable[_DOC]): 文档集合

    Returns:
        `List[_DOC]`: 排序后的文档对象集合
    """
    doc_map = {str(r.id): r for r in docs}
    return [doc_map[key] for key in keys]


class DepartmentLoader(DataLoader[str, DepartmentModel]):
    """定义 `DepartmentModel` 类型的 Loader 类"""

    async def batch_load_fn(self, keys: Iterable[str]) -> ListType[DepartmentModel]:
        """批量读取部门数据

        Args:
            keys (Iterable[str]): Key 集合迭代器对象

        Returns:
            Promise[List[DepartmentModel]]: 异步对象, 可获取 `DepartmentModel` 实体类对象集合
        """
        return _order_by_keys(keys, DepartmentModel.objects(id__in=keys))


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
        return _order_by_keys(keys, EmployeeModel.objects(id__in=keys))


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
        return _order_by_keys(keys, RoleModel.objects(id__in=keys))


# 实例化 Dataloader 对象
role_loader = RoleLoader()
