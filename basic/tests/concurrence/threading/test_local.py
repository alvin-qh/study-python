"""测试线程本地对象

线程本地对象即可为每个线程保存一组值, 且这组值只在当前线程生效
"""

import threading
from typing import Any, cast

from pytest import raises
from werkzeug.local import Local, LocalProxy, release_local


def test_python_thread_local() -> None:
    """测试 Python 内置的线程本地对象"""
    # 实例化线程本地对象
    loc = threading.local()

    # 设置主线程本地对象的 n 值
    loc.n = 100

    def func() -> None:
        """线程入口函数"""
        try:
            # 改变子线程本地对象的 n 值
            loc.n = 200
            assert loc.n == 200
        finally:
            # 清理线程本地存储
            loc.__dict__.clear()

    # 启动线程
    t = threading.Thread(target=func)
    t.start()
    t.join()

    # 主线程的 n 值不受子线程影响
    assert loc.n == 100

    # 清理线程本地存储
    loc.__dict__.clear()


def test_werkzeug_local() -> None:
    """测试本地线程存储

    通过 `werkzeug.local` 包下的 `Local` 类可以保存线程本地存储, 相比 Python 内置的 `local` 类型, `werkzeug` 库支持更多的并发场景,
    包括进程, 线程和协程
    """
    loc = Local()

    # 设置主线程本地对象的 n 值
    loc.n = 100

    def func() -> None:
        """线程入口函数"""
        try:
            # 改变子线程本地对象的 n 值
            loc.n = 200
            assert loc.n == 200
        finally:
            # 清理线程本地存储
            release_local(loc)

    # 启动线程
    t = threading.Thread(target=func)
    t.start()
    t.join()

    # 主线程的 n 值不受子线程影响
    assert loc.n == 100

    # 清理线程本地存储
    release_local(loc)


def test_werkzeug_local_proxy() -> None:
    """测试本地线程代理

    通过 `werkzeug.local` 包下的 `LocalProxy` 类可以对 `Local` 中如何存取内容进行代理设置。 代理的方式有两种:
    - 对 `Local` 中的内容存储定义代理快捷方式;
    - 提供获取 `Local` 存储内容的代理方法
    """
    h: Any

    class Holder:
        """测试 LocalProxy 的类"""

        def __init__(self, n: int = 0) -> None:
            """保存一个整数值"""
            self.n = n

    # 定义线程本地对象
    loc = Local()

    # 测试 LocalProxy 作为 Local 存储内容的快捷访问

    # 在 Local 对象中存储 Holder 对象
    loc.holder = Holder()

    # 生成 LocalProxy 对象, 表示对 loc.holder 的快捷访问
    # 即对 h 变量的访问等同于对 loc.holder 的访问
    h = loc("holder")  # 完整写法为 holder = LocalProxy(loc, "holder")
    assert h.n == 0  # 相当于获取 loc.holder.n 的值

    h.n = 100  # 相当于 loc.holder.n = 100
    assert h.n == 100

    # 释放线程本地存储
    release_local(loc)
    # 此时在通过 h 变量访问会出错
    # h.n 相当于 loc.holder.n, 但由于 loc 内容已被释放 (已经不存在 "holder"), 所以访问失败
    with raises(RuntimeError) as e:
        assert h.n

    # 确认失败的原因
    assert (
        str(e.value) == "no object bound to holder"
        or str(e.value) == "object is not bound"
    )

    """测试 LocalProxy 作为 Local 内容访问的代理方法"""

    def get_local_value() -> Holder:
        """定义一个代理方法用于存储 Local 对象"""
        # 判断 Local 对象中是否存在以 "holder" 命名的内容
        if not hasattr(loc, "holder"):
            # 如果无 "holder", 则新建一个名为 "holder" 的存储
            loc.holder = Holder()

        return cast(Holder, loc.holder)

    # 设置 get_local_value 函数为代理方法
    h = LocalProxy(get_local_value)
    assert h.n == 0  # h.n 访问相当于对 get_local_value 函数返回值对象的 n 属性进行访问

    h.n = 100
    assert h.n == 100

    # 此时释放 Local 内容不会影响到 h 代理的使用
    # 因为 get_local_value 函数内部会重建 Local 存储
    release_local(loc)
    assert h.n == 0
