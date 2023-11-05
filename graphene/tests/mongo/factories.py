import factory
from factory.mongoengine import MongoEngineFactory
from mongo.models import Department, Employee, Org, Role


class BaseFactory(MongoEngineFactory):
    """模型工厂类超类"""

    class Meta:
        pass


class OrgModelFactory(BaseFactory):
    """组织模型工厂类"""

    class Meta:
        model = Org

    name: str = factory.Sequence(lambda n: f"Org-{n}")


class DepartmentModelFactory(BaseFactory):
    """部门模型工厂类"""

    class Meta:
        model = Department

    name: str = factory.Sequence(lambda n: f"Department-{n}")


class RoleModelFactory(BaseFactory):
    """角色模型工厂类"""

    class Meta:
        model = Role


class EmployeeModelFactory(BaseFactory):
    """员工模型工厂类"""

    class Meta:
        model = Employee

    name: str = factory.Sequence(lambda n: f"Employee-{n}")
