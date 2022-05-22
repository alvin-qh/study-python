from pytest import raises

from .context import Context


def test_context_scope() -> None:
    with Context() as ctx:
        ctx.put("A", 100)
        ctx.put("B", 200)

        assert ctx.get("A") == 100
        assert ctx.get("B") == 200

    with raises(KeyError):
        assert ctx.get("A")

    with raises(KeyError):
        assert ctx.get("B")


def test_context_with_exception() -> None:
    with Context(deliver_exc=True) as ctx:
        raise ValueError("error")

    assert ctx.exception[0] is ValueError
    assert str(ctx.exception[1]) == "error"
