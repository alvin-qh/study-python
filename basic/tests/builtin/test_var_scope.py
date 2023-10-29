from pytest import raises


def test_locals_function() -> None:
    """
    `locals` 函数用于获取所有局部变量组成的字典对象
    """
    # 定义两个局部变量
    a = 1
    b = 2

    # 获取当前所有局部变量组成的字典对象
    assert locals() == {"a": 1, "b": 2}


# 定义两个全局变量
g_a = 1
g_b = 2


def test_globals_function() -> None:
    """
    `globals` 函数用于获取所有的全局变量组成的字典对象
    """
    assert "g_a" in globals()
    assert "g_b" in globals()


def test_local_keyword_in_closure() -> None:
    """
    测试在闭包函数中使用 `nonlocal` 访问外部函数定义的局部变量

    函数定义的局部变量, 在函数内部的闭包函数中只能读取而无法修改.
    如需修改, 则需要通过 `nonlocal` 关键字进行授权
    """
    # 定义局部变量
    a = 1

    def closure() -> None:
        """
        定义一个闭包函数, 对外层局部变量进行读写操作

        不使用 `nonlocal` 关键字, 无法修改局部变量
        """
        # 闭包函数中可以读取外部定义的局部变量
        assert a == 1  # noqa

        # 闭包函数中无法直接修改外部定义的局部变量, 会抛出 UnboundLocalError 异常
        a = 2  # noqa

    # 调用闭包函数, 会抛出异常, 表示闭包函数内修改了外部的局部变量
    with raises(UnboundLocalError):
        closure()

    # 闭包函数内未改变局部变量 a
    assert a == 1

    def closure_nonlocal() -> None:
        """
        定义一个闭包函数, 对外层局部变量进行读写操作
        """
        # 为外部函数的局部变量 a 授予修改权限
        nonlocal a

        # 读取外部局部变量
        assert a == 1
        # 修改外部局部变量
        a = 2

    # 调用闭包函数
    closure_nonlocal()

    # 确认具备变量在闭包函数内被修改
    assert a == 2


# 定义全局变量
g_a = 1


def func() -> None:
    """
    对全局变量进行读写操作

    不使用 `global` 关键字, 无法修改全局变量
    """
    # 读取全局变量
    assert g_a == 1  # noqa

    # 修改全局变量, 因为未使用 global 关键字, 抛出 UnboundLocalError 异常
    g_a = 2  # noqa


def func_global() -> None:
    """
    对全局变量进行读写操作

    使用 `global` 关键字, 可以修改全局变量
    """
    # 为全局变量 g_a 授予修改权限
    global g_a

    # 测试读取全局变量
    assert g_a == 1
    # 修改全局变量
    g_a = 2


def test_global_keyword() -> None:
    """
    测试 `global` 关键字在函数内部访问全举变量

    定义的全局变量, 在函数内部只能读取而无法修改.
    如需修改, 则需要通过 `global` 关键字进行授权
    """
    # 调用函数, 会抛出异常, 表示在函数内部无法直接修改全局变量
    with raises(UnboundLocalError):
        func()

    # 函数内部未修改全局变量
    assert g_a == 1

    # 调用函数, 函数内部通过 global 关键字修改全局变量
    func_global()
    assert g_a == 2
