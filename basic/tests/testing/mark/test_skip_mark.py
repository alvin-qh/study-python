from typing import NoReturn

from pytest import fail, mark

from basic.testing.mark import VERSION


@mark.skip(reason="Skip test")
def test_skip() -> None:
    """
    `@skip` 装饰器表示该测试会被跳过
    - `reason`: 参数表示跳过的原因
    """
    fail()


@mark.skipif(condition=(VERSION == 3), reason="Skip if version matched")
def test_skipif_not_run() -> None:
    """
    `@skipif` 装饰器表示有条件的跳过测试, 即条件为 `True` 时跳过
    - `condition`: 跳过测试的条件
    - `reason`: 跳过测试的原因
    """
    fail()


@mark.skipif(condition=(VERSION > 3), reason="Run if version not match")
def test_skipif_run() -> None:
    """
    `skipif` 条件为 `False` 时执行此测试
    """


# skip 用于函数时, 返回一个装饰器, 被此装饰器装饰的测试会被跳过
skipmark = mark.skip(reason="Skip this test")


@skipmark
def test_skipmark() -> NoReturn:
    """
    被 `skipmark` 变量引用的装饰器修饰, 该测试被跳过
    """
    fail()


# 调用 skipif 函数, 返回一个装饰器, 凡符合设定条件, 被装饰的测试会被跳过
skipifmark = mark.skipif(
    condition=(VERSION == 3),
    reason="Skip if version matched",
)


@skipifmark
def test_skipifmark() -> NoReturn:
    """
    被 `skipifmark` 变量引用的装饰器修饰, 该测试被跳过
    """
    fail()
