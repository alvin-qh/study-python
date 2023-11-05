from peewee_.core import Tenant, User, context


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


def test_current_user_context() -> None:
    class FakeUser(User):
        mark = "Fake User"

    with context.with_current_user(FakeUser()):
        user: FakeUser = context.get_current_user()
        assert user is not None
        assert user.mark == "Fake User"

    assert context.get_current_user() is None
