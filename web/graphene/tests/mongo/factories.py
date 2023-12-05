import factory.faker
import factory.fuzzy
from factory.mongoengine import MongoEngineFactory
from mongo import DepartmentModel, EmployeeModel, OrgModel, RoleModel


class BaseFactory(MongoEngineFactory):
    """匹配 mongo engine 框架的工厂类"""

    class Meta:
        """工厂元数据类"""


class OrgModelFactory(BaseFactory):
    """组织模型工厂类"""

    class Meta:
        # 定义实体类型
        model = OrgModel

    # 组织名称属性
    name: str = factory.faker.Faker("name")


class DepartmentModelFactory(BaseFactory):
    """部门模型工厂类"""

    class Meta:
        # 定义实体类型
        model = DepartmentModel

    # 部门名称属性
    name: str = factory.faker.Faker("name")

    # 部门级别属性
    level: int = factory.fuzzy.FuzzyInteger(1, 10)


class RoleModelFactory(BaseFactory):
    """角色模型工厂类"""

    class Meta:
        # 定义实体类型
        model = RoleModel


class EmployeeModelFactory(BaseFactory):
    """员工模型工厂类"""

    class Meta:
        # 定义实体类型
        model = EmployeeModel

    # 员工姓名属性
    name: str = factory.faker.Faker("name")
