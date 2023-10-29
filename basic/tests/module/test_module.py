from importlib import import_module


def test_static_import() -> None:
    """
    测试静态导入
    """
    # 静态导入所需的标识
    from module import Class, function, value

    # 函数导入
    assert function() == "1.0"

    # 类导入
    c = Class(100)
    assert c.a == 100

    # 变量导入
    assert value == 0


def test_dynamic_import() -> None:
    """
    使用 `import_module` 函数动态导入模块
    """
    # 使用绝对层级导入
    m = import_module("module.plugin1")
    assert m.__name__ == "module.plugin1"

    # 使用相对层级导入
    # __package__ 表示相对于当前包
    # m = import_module("module.plugin1", package=__package__)

    # 从导入的模块实例化对象
    plugin = m.Plugin()
    assert plugin.display() == "Hello"

    # 导入另一个包
    m = import_module("module.plugin2")

    plugin = m.Plugin()
    assert plugin.display() == "World"


def test_builtin_import() -> None:
    """
    使用内置的 `__import__` 函数导入包

    `__import__` 函数的作用是导入包 (而非模块), 并且需要指定本次导入要使用的模块
    """
    # 导入包, 并指定使用 plugin1 和 plugin2 两个模块
    # 注意: 如果省略了 fromlist 参数, 则不会导入 sub 包, 只会导入 module_ 包
    m = __import__("module", fromlist=["plugin1", "plugin2"])
    assert m.__name__ == "module"

    # 从导入的模块实例化对象
    plugin = m.plugin1.Plugin()
    assert plugin.display() == "Hello"

    # 从导入的模块实例化对象
    plugin = m.plugin2.Plugin()
    assert plugin.display() == "World"
