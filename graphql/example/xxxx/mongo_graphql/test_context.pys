from mongo_graphql.core.context import context, run_once
from mongo_graphql.models import Org


class TestContext:
    def test_context_get_set(self):
        context.a = 100
        assert context.a == 100

    def test_context_delete(self):
        context.a = 100
        del context.a
        assert context.a is None

    def test_tenant_context(self):
        org = Org()
        with context.with_tenant_context(org):
            assert context.get_current_org() == org

        assert context.get_current_org() is None


def test_run_once():
    run_times = 0

    @run_once
    def run_once_func():
        nonlocal run_times
        run_times += 1
        assert run_times == 1
        return run_times

    assert run_once_func() == 1
    assert run_once_func() == 1
