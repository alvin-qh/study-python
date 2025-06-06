from pytest import fail, skip

from basic.testing.mark import VERSION

# skip 函数用于跳过之后的测试，可以用于 function, method 或整个 module


def test_skip_function() -> None:
    """
    根据版本号选择跳过当前测试函数
    """
    if VERSION >= 3:
        skip(reason="Version not match")

    fail()


if VERSION >= 3:
    # 根据版本号选择跳过当前测试模块
    skip("Version not match", allow_module_level=True)


def test_skip_module() -> None:
    """
    该测试方法不会执行 (因为整个模块被跳过)
    """
    fail()
