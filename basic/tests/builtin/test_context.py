from builtin import Context
from pytest import raises
from builtin.context import random_number_context


def test_context_scope() -> None:
    """测试上下文范围和上下文对象"""
    # 产生一个上下文对象并调用 __enter__ 方法进入上下文范围
    # 退出上下文范围后会调用上下文对象的 __exit__ 方法
    with Context() as ctx:
        ctx.put("A", 100)
        ctx.put("B", 200)

        assert ctx.get("A") == 100
        assert ctx.get("B") == 200

    # 退出上下文范围后, 存储的 Key/Value 不可用
    with raises(KeyError):
        assert ctx.get("A")

    # 退出上下文范围后, 存储的 Key/Value 不可用
    with raises(KeyError):
        assert ctx.get("B")


def test_context_with_exception() -> None:
    """测试上下文范围内的异常抛出情况"""
    # 产生一个上下文对象并调用 __enter__ 方法进入上下文范围
    # suppress_exception 表示 __exit__ 方法返回 True, 异常不传递到上下文范围之外
    with Context(suppress_exception=True) as ctx:
        # 抛出异常
        raise ValueError("error")

    assert ctx.exception is not None

    # 确认 __exit__ 方法的异常参数值
    assert ctx.exception[0] is ValueError
    assert str(ctx.exception[1]) == "error"


def test_context_from_contextmanager() -> None:
    """测试上下文管理器

    测试被 `@contextmanager` 装饰器修饰的函数作为上下文管理器使用
    """
    nums = []

    while True:
        try:
            with random_number_context() as n:
                nums.append(n)
        except IndexError as e:
            assert e.args[0] == "random number out of range"
            break

    assert sorted(nums) == [1, 2, 3, 4, 5, 6, 7]
