import factory
from factory import Factory

from peewee_graphql.models import (
    Org,
    Department,
    Role,
    Employee
)


class PeeweeFactory(Factory):
    class Meta:
        model = None

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        return cls.Meta.model(*args, **kwargs)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        instance = cls._meta.model(**kwargs)
        instance.save()
        return instance


class OrgFactory(PeeweeFactory):
    class Meta:
        model = Org

    name: str = factory.Sequence(lambda n: f"Org-{n}")


class DepartmentFactory(PeeweeFactory):
    class Meta:
        model = Department

    name: str = factory.Sequence(lambda n: f"Department-{n}")


class RoleFactory(PeeweeFactory):
    class Meta:
        model = Role

    name: str = "member"


class EmployeeFactory(PeeweeFactory):
    class Meta:
        model = Employee

    name: str = factory.Sequence(lambda n: f"Employee-{n}")
    gender: str = "M"
