from mongo.core import context
from mongo.models import Org


def test_context_get_set() -> None:
    context.a = 100
    assert context.a == 100


def test_context_delete() -> None:
    context.a = 100
    del context.a
    assert context.a is None


def test_tenant_context() -> None:
    org = Org()
    with context.with_tenant_context(org):
        assert context.get_current_tenant() == org

    assert context.get_current_tenant() is None
