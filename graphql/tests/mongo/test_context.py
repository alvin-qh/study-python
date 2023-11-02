from mongo.core.context import context, run_once
from mongo.models import Org


class TestContext:
    def test_context_get_set(self) -> None:
        context.a = 100
        assert context.a == 100

    def test_context_delete(self) -> None:
        context.a = 100
        del context.a
        assert context.a is None

    def test_tenant_context(self) -> None:
        org = Org()
        with context.with_tenant_context(org):
            assert context.get_current_org() == org

        assert context.get_current_org() is None


def test_run_once() -> None:
    run_times = 0

    @run_once
    def run_once_func() -> int:
        nonlocal run_times
        run_times += 1

        assert run_times == 1
        return run_times

    assert run_once_func() == 1
    assert run_once_func() == 1
