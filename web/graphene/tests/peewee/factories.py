from typing import Any, List, Type

import factory.faker
import factory.fuzzy
from peewee import Model
from peewee_ import DepartmentModel, EmployeeModel, OrgModel, RoleModel


class PeeweeOptions(factory.base.FactoryOptions):
    """定义 Peewee 工厂属性"""

    def _build_default_options(self) -> List[factory.base.OptionDefault]:
        """为工厂构建默认属性值

        Returns:
            `List[factory.base.OptionDefault]`: 返回工厂默认属性集合
        """
        defaults: List[factory.base.OptionDefault] = super()._build_default_options()
        return defaults + []


class PeeweeFactory(factory.base.Factory):
    """定义 Peewee 工厂类型, 用于自动构建 Peewee 实体对象"""

    # 指定提供工厂属性的类型
    _options_class = PeeweeOptions

    class Meta:
        """定义工厂类型元数据"""

    @classmethod
    def _create(cls, model_class: Type[Model], *args: Any, **kwargs: Any) -> Any:
        """定义实体创建方法

        Args:
            - `model_class` (`Type[Model]`): 要创建的实体对象的类型

        Returns:
            Any: 被创建的实体对象
        """
        # 创建实体对象
        model = model_class(*args, **kwargs)

        # 实体对象持久化
        model.save()

        return model


class OrgModelFactory(PeeweeFactory):
    """组织模型工厂类"""

    class Meta:
        # 定义实体类型
        model = OrgModel

    # 组织名称属性
    name: str = factory.faker.Faker("name")


class DepartmentModelFactory(PeeweeFactory):
    """部门模型工厂类"""

    class Meta:
        # 定义实体类型
        model = DepartmentModel

    # 部门名称属性
    name: str = factory.faker.Faker("name")

    # 部门级别属性
    level: int = factory.fuzzy.FuzzyInteger(1, 10)


class RoleModelFactory(PeeweeFactory):
    """角色模型工厂类"""

    class Meta:
        # 定义实体类型
        model = RoleModel


class EmployeeModelFactory(PeeweeFactory):
    """员工模型工厂类"""

    class Meta:
        # 定义实体类型
        model = EmployeeModel

    # 员工姓名属性
    name: str = factory.faker.Faker("name")
