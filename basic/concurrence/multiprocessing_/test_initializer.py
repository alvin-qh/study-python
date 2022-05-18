from ctypes import c_bool, c_int
from multiprocessing import Pool, Value
from typing import List, Tuple

# 全局变量, 每个进程的内存空间都会具备
_values: List[Tuple[Value, Value]] = None


def _initializer(values: List[Tuple[Value, Value]]) -> None:
    """
    进程池初始化函数

    Args:
        values (List[Tuple[Value, Value]]): 进程池初始化参数, Value 对象列表
    """
    global _values

    # 这个赋值操作相当于为每个进程的 _values 全局变量进行复制
    # 此时每个子进程的内存空间中都会存在一个 Value 列表对象的副本
    _values = values


def _is_prime(n: int) -> None:
    """
    进程池入口函数

    在进程池中判断参数 `n` 是否为质数

    通过每个子进程内存空间的全局变量 `ctx`, 将结果进行保存, 由于 `ctx` 对象内部存储的 `Value`
    类型对象, 对其进行的操作会在各个进程中共享

    Args:
        n (int): 要判断是否为质数的数
    """
    num, val = _values[n]
    # 由于每个进程只会进行一次初始化操作
    # 且因为进程池会复用进程, 所以这里对某个进程的公共变量操作, 可能会在复用该进程时影响到
    # 对公共变量的访问
    # values.clear()

    num.value = n

    if n <= 1:
        # 设置结果值
        val.value = False
        return

    for i in range(2, n):
        if n % i == 0:
            # 设置结果值
            val.value = False
            return

    # 设置结果值
    val.value = True


def test_pool_initializer() -> None:
    """
    进程池 (`Pool` 对象) 和子进程 (`Process` 对象) 的不同之处在于:
    - 子进程是在代码上下文中产生的, 子进程在产生后, 可以继承之前的内存空间
    - 进程池则不具备这种特征, 无法通过进程间传参的方式传递同步对象 (例如 `Value` 类型对象)

    所以 `Pool` 构造器提供了一个 `initializer` 方法参数, 在进程池产生时会在各个子进程中执行该方法
    起到为进程池中每个子进程进行初始化的目的

    注意:
    - 进程池会复用进程, 所以一个进程对全局内存的操作可能会在该进程复用时影响到进程访问公共变量
    """
    # 声明 Value 对象列表, 这个变量是在主进程内存地址空间中产生
    values = [(Value(c_int), Value(c_bool)) for _ in range(10)]

    # 实例化进程池, 执行 _pooled_initializer 方法为每个子进程进行初始化, 传递初始化参数
    with Pool(initializer=_initializer, initargs=(values,)) as pool:
        pool.starmap(_is_prime, zip(range(10)))

    # 结果转换为普通值
    results = [(v[0].value, v[1].value) for v in values]
    results.sort(key=lambda x: x[0])

    # 确保结果符合预期
    assert results == [
        (0, False),
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (5, True),
        (6, False),
        (7, True),
        (8, False),
        (9, False),
    ]
