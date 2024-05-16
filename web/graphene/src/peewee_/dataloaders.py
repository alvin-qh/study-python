from typing import Iterable
from typing import List
from typing import List as ListType
from typing import TypeVar

from aiodataloader import DataLoader

from .core import BaseModel
from .models import Department as DepartmentModel
from .models import Employee as EmployeeModel
from .models import Role as RoleModel

_MODEL = TypeVar("_MODEL", bound=BaseModel)


def _order_by_keys(ids: Iterable[int], models: Iterable[_MODEL]) -> List[_MODEL]:
    """将查询结果按照所给的 `ids` 的顺序进行排列

    Args:
        - `ids` (Iterable[int]): id 集合, 对应着 `models` 参数集合中各个实体对象的 id 属性
        - `models` (Iterable[_MODEL]): 实体对象集合

    Returns:
        `List[_MODEL]`: 排序后的实体对象集合
    """
    doc_map = {model.id: model for model in models}
    return [doc_map[key] for key in ids]


class DepartmentLoader(DataLoader[str, DepartmentModel]):
    """定义 `DepartmentModel` 类型的 Loader 类"""

    async def batch_load_fn(self, keys: Iterable[str]) -> ListType[DepartmentModel]:
        """批量读取部门数据

        Args:
            keys (Iterable[str]): Key 集合迭代器对象

        Returns:
            Promise[List[DepartmentModel]]: 异步对象, 可获取 `DepartmentModel` 实体类对象集合
        """
        ids = [int(id_) for id_ in keys]
        return _order_by_keys(
            ids, DepartmentModel.select().where(DepartmentModel.id.in_(ids))
        )


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
        ids = [int(id_) for id_ in keys]
        return _order_by_keys(
            ids, EmployeeModel.select().where(EmployeeModel.id.in_(ids))
        )


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
        ids = [int(id_) for id_ in keys]
        return _order_by_keys(ids, RoleModel.select().where(RoleModel.id.in_(ids)))


# 实例化 Dataloader 对象
role_loader = RoleLoader()
