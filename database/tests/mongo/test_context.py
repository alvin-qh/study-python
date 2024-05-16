from mongo.engine.core import context
from peewee_.core.context import Tenant


def test_get_set_context_attribute() -> None:
    context.name = "Alvin"

    name = context.name
    assert name == "Alvin"

    name = context["name"]
    assert name == "Alvin"


def test_delete_context_attribute() -> None:
    context.name = "Alvin"
    del context.name

    assert context.name is None

    context.name = "Alvin"
    del context["name"]

    assert context.name is None


def test_tenant_context() -> None:
    class FakeTenant(Tenant):
        mark = "Fake Tenant"

    with context.with_tenant_context(FakeTenant()):
        assert context.get_current_tenant().mark == "Fake Tenant"

    assert context.get_current_tenant() is None
