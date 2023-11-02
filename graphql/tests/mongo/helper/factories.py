import factory
from factory.mongoengine import MongoEngineFactory
from mongo.models import Department, Employee, Org, Role


class BaseFactory(MongoEngineFactory):
    class Meta:
        pass

    pass


class OrgFactory(BaseFactory):
    class Meta:
        model = Org

    name: str = factory.Sequence(lambda n: f"Org-{n}")


class DepartmentFactory(BaseFactory):
    class Meta:
        model = Department

    name: str = factory.Sequence(lambda n: f"Department-{n}")


class RoleFactory(BaseFactory):
    class Meta:
        model = Role


class EmployeeFactory(BaseFactory):
    class Meta:
        model = Employee

    name: str = factory.Sequence(lambda n: f"Employee-{n}")
