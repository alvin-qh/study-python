from peewee_ import OrgModel, context


def test_context_get_set() -> None:
    context.a = 100
    assert context.a == 100


def test_context_delete() -> None:
    context.a = 100
    del context.a
    assert context.a is None


def test_tenant_context() -> None:
    org = OrgModel()
    with context.with_tenant_context(org):
        assert context.get_current_tenant() is org

    assert context.get_current_tenant() is None
