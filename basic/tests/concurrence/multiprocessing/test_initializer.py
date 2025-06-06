from ctypes import c_bool, c_int
from multiprocessing import Pool, Value

from basic.concurrence.multiprocessing.prime import (
    initializer,
    is_prime_by_global_variable,
)


def test_pool_initializer() -> None:
    """测试进程池初始化函数

    进程池 (`Pool` 对象) 和子进程 (`Process` 对象) 的不同之处在于:

    - 子进程是在代码上下文中产生的, 子进程在产生后, 可以继承之前的内存空间
    - 进程池则不具备这种特征, 无法通过进程间传参的方式传递同步对象 (例如 `Value` 类型对象)

    所以 `Pool` 构造器提供了一个 `initializer` 方法参数, 在进程池产生时会在各个子进程中执行该方法起到为进程池中每个子进程进行初始化的目的

    注意:

    - 进程池会复用进程, 所以一个进程对全局内存的操作可能会在该进程复用时影响到进程访问公共变量
    """
    # 声明 Value 对象列表, 这个变量是在主进程内存地址空间中产生
    values = [(Value(c_int), Value(c_bool)) for _ in range(10)]

    # 实例化进程池, 执行 _pooled_initializer 方法为每个子进程进行初始化, 传递初始化参数
    with Pool(initializer=initializer, initargs=(values,)) as pool:
        pool.starmap(is_prime_by_global_variable, zip(range(10)))

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
