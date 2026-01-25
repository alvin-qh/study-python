import inspect
import json
import time
from dataclasses import dataclass
from functools import (
    cache,
    cached_property,
    cmp_to_key,
    lru_cache,
    partial,
    partialmethod,
    reduce,
    singledispatch,
    singledispatchmethod,
    total_ordering,
    update_wrapper,
    wraps,
)
from operator import add
from typing import Any, Self


def test_partial_function_with_function() -> None:
    """测试 `partial` 函数

    `partial` 函数用于创建一个偏函数, 偏函数会预设部分参数, 当调用偏函数时, 剩余的参数会传入原函数执行

    本例中, 通过 `partial` 函数将一个函数包装为一个偏函数, 并预设其第一个参数
    """
    # 将 `add` 创建包装为一个偏函数, 并预设其第一个参数
    fn = partial(add, 100)

    # 调用偏函数, 传入第二个参数, 确认执行结果为 `add` 函数的第一个预设参数和第二个参数之和
    assert fn(1) == 101


def test_partial_function_with_object_method() -> None:
    """测试 `partial` 函数

    `partial` 函数用于创建一个偏函数, 偏函数会预设部分参数, 当调用偏函数时, 剩余的参数会传入原函数执行

    本例中, 通过 `partial` 函数将对象的一个方法包装为一个偏函数, 并预设其第一个参数
    """

    # 创建一个类, 并定义一个方法
    class Test:
        def add(self, a: int, b: int) -> int:
            return a + b

    # 创建 `Test` 类的一个对象
    t = Test()

    # 将 `Test.add` 方法包装为一个偏函数, 并预设其第一个参数
    fn = partial(t.add, 100)

    # 调用偏函数, 传入第二个参数, 确认执行结果为 `Test.add` 方法的参数和第二个参数之和
    assert fn(1) == 101


def test_partial_function_with_classmethod() -> None:
    """测试 `partial` 函数

    `partial` 函数用于创建一个偏函数, 偏函数会预设部分参数, 当调用偏函数时, 剩余的参数会传入原函数执行

    本例中, 通过 `partial` 函数将对象的一个类方法包装为一个偏函数, 并预设其第一个参数
    """

    # 创建一个类, 并定义一个类方法
    class Test:
        @classmethod
        def add(cls, a: int, b: int) -> int:
            return a + b

    # 将 `Test.add` 方法包装为一个偏函数, 并预设其第一个参数
    fn = partial(Test.add, 100)

    # 调用偏函数, 传入第二个参数, 确认执行结果为 `Test.add` 方法的参数和第二个参数之和
    assert fn(1) == 101


def test_partial_method_with_staticmethod() -> None:
    """测试 `partial` 函数

    `partial` 函数用于创建一个偏函数, 偏函数会预设部分参数, 当调用偏函数时, 剩余的参数会传入原函数执行

    本例中, 通过 `partial` 函数将对象的一个静态方法包装为一个偏函数, 并预设其第一个参数
    """

    # 创建一个类, 并定义一个静态方法
    class Test:
        @staticmethod
        def add(a: int, b: int) -> int:
            return a + b

    # 将 `Test.add` 方法包装为一个偏函数, 并预设其第一个参数
    fn = partial(Test.add, 100)

    # 调用偏函数, 传入第二个参数, 确认执行结果为 `Test.add` 方法的参数和第二个参数之和
    assert fn(1) == 101


def test_partial_method_with_lambda() -> None:
    """测试 `partial` 函数

    `partial` 函数用于创建一个偏函数, 偏函数会预设部分参数, 当调用偏函数时, 剩余的参数会传入原函数执行

    本例中, 通过 `partial` 函数将对象的一个属性包装为一个偏函数, 并预设其第一个参数
    """
    # 将 `lambda` 创建包装为一个偏函数, 并预设其第一个参数
    fn = partial(lambda a, b: a + b, 100)

    # 调用偏函数, 传入第二个参数, 确认执行结果为 `lambda` 函数的参数和第二个参数之和
    assert fn(1) == 101


def test_create_partial_method_in_class() -> None:
    """测试创建偏函数在类中的使用

    通过 `partialmethod` 函数可以将偏函数定义为指定类的方法

    和 `partial` 函数不同, `partialmethod` 函数在包装目标函数时, 默认会将第一个参数作为 `self` 参数,
    所以只能在某个类中使用 `partialmethod` 函数来为这个类创建一个偏函数

    和 `partial` 函数类似, `partialmethod` 函数的参数为要包装的目标函数以及目标函数中已确定的参数,
    目标函数即可以是当前类的方法, 也可以是类外的其它函数, 对于前者可以直接包装, 对于后者, 要确定目标函数的第一个参数必须为一个对象类型

    对于类的其它方法, 如类方法, 静态方法, 则无法通过 `partialmethod` 函数来包装偏函数
    """

    def add(self: Any, a: int, b: int) -> int:
        """测试通过 `partialmethod` 函数为 `Calculator` 类创建偏函数的目标函数

        该函数在 `Calculator` 类外定义, 仍可通过 `partialmethod` 函数来包装偏函数

        注意, 第一个参数必须为对象类型, 否则无法通过 `partialmethod` 函数来包装偏函数
        """
        return a + b

    class Calculator:
        """测试通过 `partialmethod` 函数创建偏函数的类"""

        def multiply(self, a: int, b: int) -> int:
            """用于测试 `partialmethod` 函数创建偏函数的目标方法

            该方法在 `Calculator` 类内定义, 可直接通过 `partialmethod` 函数来包装偏函数
            """
            return a * b

        # 通过 `partialmethod` 函数将 `multiply` 创建包装为一个偏函数, 并预设其第一个参数
        double = partialmethod(multiply, 2)

        # 通过 `partialmethod` 函数将 `multiply` 创建包装为一个偏函数, 并预设其第一个参数
        triple = partialmethod(multiply, 3)

        # 通过 `partialmethod` 函数将 `add` 创建包装为一个偏函数, 并预设其第一个参数
        increment = partialmethod(add, 1)

    # 创建 `Calculator` 类的一个对象
    calc = Calculator()

    # 确认执行结果为 `multiply` 方法的参数和第二个参数的乘积
    assert calc.double(2) == 4

    # 确认执行结果为 `multiply` 方法的参数和第二个参数的乘积
    assert calc.triple(2) == 6

    # 确认执行结果为 `add` 方法的参数和第二个参数之和
    assert calc.increment(2) == 3


def test_comp_to_key_from_compare_function() -> None:
    """测试 `cmp_to_key` 函数

    `cmp_to_key` 函数用于将一个比较函数转换为一个键函数, 键函数可以用于排序列表

    本例中, 通过 `cmp_to_key` 函数将一个比较函数转换为一个键函数, 然后将列表排序
    """
    # 定义乱序集合
    nums = [1, 5, 2, 4, 3]

    # 通过 `cmp_to_key` 函数将一个比较函数转换为一个键函数
    nums.sort(key=cmp_to_key(lambda a, b: a - b))  # type: ignore[operator]

    # 确认排序结果为升序
    assert nums == [1, 2, 3, 4, 5]


def test_cmp_to_key_from_object() -> None:
    """测试 `cmp_to_key` 函数

    `cmp_to_key` 函数用于将一个比较函数转换为一个键函数, 键函数可以用于排序列表

    本例中, 通过 `cmp_to_key` 函数将一个比较函数转换为一个键函数, 然后将列表排序
    """

    # 创建一个数据类型, 具备两个属性值
    @dataclass
    class Value:
        a: int
        b: int

    # 创建一个 `Value` 类对象集合
    vals = [
        Value(1, 5),
        Value(5, 2),
        Value(2, 4),
        Value(4, 3),
    ]

    def _compare_value_object(a: Value, b: Value) -> int:
        """比较两个 `Value` 类对象

        本例中, 通过比较两个 `Value` 类对象的属性值, 返回一个整数, 用于排序列表

        Args:
            a (`Value`): 第一个 `Value` 类对象
            b (`Value`): 第二个 `Value` 类对象

        Returns:
            `int`: 比较结果
        """
        v = a.a - b.a
        if v == 0:
            v = a.b - b.b
        return v

    # 通过 `cmp_to_key` 函数将一个对象比较函数转换为一个键函数
    vals.sort(key=cmp_to_key(_compare_value_object))

    # 确认排序结果为升序
    assert vals == [Value(1, 5), Value(2, 4), Value(4, 3), Value(5, 2)]


def test_reduce_function() -> None:
    """测试 `reduce` 函数

    `reduce` 函数用于将一个序列中的元素进行累积计算, 返回一个结果

    本例中, 通过 `reduce` 函数将一个序列中的元素进行累积计算, 返回一个结果
    """
    # 创建一个整数序列
    nums = [n for n in range(1, 101)]

    # 通过 `reduce` 函数将一个序列中的元素进行累积计算, 返回一个结果
    res = reduce(lambda a, b: a + b, nums)

    # 确认计算结果为 5050
    assert res == 5050


def test_reduce_function_with_initializer() -> None:
    """测试 `reduce` 函数

    `reduce` 函数用于将一个序列中的元素进行累积计算, 返回一个结果

    本例中, 通过 `reduce` 函数将一个序列中的元素进行累积计算, 添加初始值, 返回一个结果
    """
    # 创建一个整数序列
    nums = [n for n in range(1, 101)]

    # 通过 `reduce` 函数将一个序列中的元素进行累积
    res = reduce(lambda a, b: a + b, nums, 100)

    # 确认计算结果为 5150
    assert res == 5150


def test_reduce_function_with_object() -> None:
    """测试 `reduce` 函数

    `reduce` 函数用于将一个序列中的元素进行累积计算, 返回一个结果

    本例中, 通过 `reduce` 函数将一个序列中的元素进行累积计算, 添加初始值, 添加对象, 添加对象方法, 添加对象属性, 添加对象属性方法, 添加对象属性方法参数
    返回一个结果
    """

    # 创建一个数据类型, 具备两个属性值
    @dataclass
    class Value:
        a: int
        b: int

        def add(self, v: Self) -> "Value":
            """添加两个 `Value` 类对象

            Args:
                v (`Value`): 第二个 `Value` 类对象

            Returns:
                `Value`: 添加结果
            """
            a = self.a + v.a
            b = self.b + v.b
            return Value(a, b)

    # 创建一个 `Value` 类对象集合
    vals = [
        Value(1, 5),
        Value(5, 2),
        Value(2, 4),
        Value(4, 3),
    ]

    # 通过 `reduce` 函数将一个序列中的元素进行累积
    res = reduce(lambda a, b: a.add(b), vals)

    # 确认计算结果为 `Value(a=12, b=14)`
    assert res == Value(12, 14)


def test_cache_decorator_on_function() -> None:
    """测试 `@cache` 装饰器用于函数

    `@cache` 装饰器用于缓存函数的结果, 以避免重复计算

    当一个函数被 `@cache` 装饰器修饰后, 则该函数上会增加几个方法, 分别为:
    - `cache_clear` 方法: 用于清除该函数上的缓存
    - `cache_info` 属性: 用于获取该函数的缓存信息
    - `cache_parameters` 方法: 用于获取创建缓存时, 所设置的缓存参数

    本例中, 通过两种方法计算斐波那契数列, 一种不加缓存, 导致所需时间比较久; 另一种通过 `cache` 装饰器缓存函数的结果,
    以避免重复计算, 计算效率较高
    """

    # 创建一个函数, 用于计算斐波那契数列
    def fib_nocache(n: int) -> int:
        if n < 2:
            return n
        return fib_nocache(n - 1) + fib_nocache(n - 2)

    # 创建一个函数, 用于计算斐波那契数列, 该函数会将每一次调用的结果缓存起来, 避免再次调用重复计算
    @cache
    def fib_cacheable(n: int) -> int:
        if n < 2:
            return n
        return fib_cacheable(n - 1) + fib_cacheable(n - 2)

    # 计算斐波那契数列并记录函数调用的时间
    start = time.perf_counter()
    assert fib_nocache(30) == 832040
    assert time.perf_counter() - start > 0.01

    # 计算斐波那契数列并记录函数调用的时间
    start = time.perf_counter()
    assert fib_cacheable(30) == 832040
    assert time.perf_counter() - start < 0.01

    # 获取函数上的缓存数据
    cache_info = fib_cacheable.cache_info()

    # 确认缓存命中次数
    assert cache_info.hits == 28
    # 确认缓存未命中次数
    assert cache_info.misses == 31
    # 确认缓存的最大数量, `None` 表示无上限
    assert cache_info.maxsize is None
    # 确认缓存的当前数量
    assert cache_info.currsize == 31

    # 获取设置函数缓存时所用的参数, 包括 `maxsize` 和 `typed`
    # 由于 `@cache` 装饰器不允许设置缓存参数, 故返回的缓存参数均为默认值
    cache_param = fib_cacheable.cache_parameters()
    assert cache_param["maxsize"] is None
    assert cache_param["typed"] is False

    # 清理 `fib_cacheable` 函数上的缓存
    fib_cacheable.cache_clear()

    # 重新计算斐波那契数列
    assert fib_cacheable(31) == 1346269


def test_cache_decorator_on_method() -> None:
    """测试 `@cache` 装饰器用于对象方法

    `@cache` 装饰器用于缓存函数的结果, 以避免函数重复计算

    当一个方法被 `@cache` 装饰器修饰后, 则该函数上会增加几个方法, 分别为:
    - `cache_clear` 方法: 用于清除该函数上的缓存
    - `cache_info` 属性: 用于获取该函数的缓存信息
    - `cache_parameters` 方法: 用于获取创建缓存时, 所设置的缓存参数

    本例中, `Fib` 类具备两个方法, 一个不加缓存, 导致所需时间比较久; 一个通过 `cache` 装饰器缓存函数的结果,
    以避免重复计算, 计算效率较高
    """

    class Fib:
        """斐波那契数列类"""

        def nocache(self, n: int) -> int:
            """计算斐波那契数列

            Args:
                n (`int`): 斐波那契数列的索引

            Returns:
                `int`: 斐波那契数列的值
            """
            if n < 2:
                return n
            return self.nocache(n - 1) + self.nocache(n - 2)

        @cache
        def cacheable(self, n: int) -> int:
            """计算斐波那契数列

            该函数通过 `cache` 装饰器缓存函数的结果, 避免重复计算, 计算效率较高

            Args:
                n (`int`): 斐波那契数列的索引

            Returns:
                `int`: 斐波那契数列的值
            """
            if n < 2:
                return n
            return self.cacheable(n - 1) + self.cacheable(n - 2)

    fib = Fib()

    # 计算斐波那契数列并记录函数调用的时间
    start = time.perf_counter()
    assert fib.nocache(30) == 832040
    assert time.perf_counter() - start > 0.01

    # 计算斐波那契数列并记录函数调用的时间
    start = time.perf_counter()
    assert fib.cacheable(30) == 832040
    assert time.perf_counter() - start < 0.01

    # 获取函数上的缓存数据
    cache_info = fib.cacheable.cache_info()

    # 确认缓存命中次数
    assert cache_info.hits == 28
    # 确认缓存未命中次数
    assert cache_info.misses == 31
    # 确认缓存的最大数量, `None` 表示无上限
    assert cache_info.maxsize is None
    # 确认缓存的当前数量
    assert cache_info.currsize == 31

    # 获取设置函数缓存时所用的参数, 包括 `maxsize` 和 `typed`
    # 由于 `@cache` 装饰器不允许设置缓存参数, 故返回的缓存参数均为默认值
    cache_param = fib.cacheable.cache_parameters()
    assert cache_param["maxsize"] is None
    assert cache_param["typed"] is False

    # 清空 `cacheable` 方法上的缓存
    fib.cacheable.cache_clear()

    # 重新计算斐波那契数列
    assert fib.cacheable(31) == 1346269


def test_lru_cache_decorator_on_function() -> None:
    """测试 `@lru_cache` 装饰器用于函数

    `@lru_cache` 装饰器也是用于缓存函数调用结果, 以避免函数重复计算, `@lru_cache` 表示缓存具备淘汰策略,
    可以在缓存数量达到最大值时, 淘汰最久未使用的缓存项

    `@lru_cache` 装饰器和 `@cache` 装饰器功能类似, 但 `@lru_cache` 具备更多参数, 例如可以设置最大缓存的数量

    当一个函数被 `@lru_cache` 装饰器修饰后, 则该函数上会增加几个方法, 分别为:
    - `cache_clear` 方法: 用于清除该函数上的缓存
    - `cache_info` 属性: 用于获取该函数的缓存信息
    - `cache_parameters` 方法: 用于获取创建缓存时, 所设置的缓存参数

    本例中, 通过两种方法计算斐波那契数列, 一种不加缓存, 导致所需时间比较久; 另一种通过 `@lru_cache` 装饰器缓存函数的结果,
    以避免重复计算, 计算效率较高
    """

    # 创建一个函数, 用于计算斐波那契数列
    def fib_nocache(n: int) -> int:
        if n < 2:
            return n
        return fib_nocache(n - 1) + fib_nocache(n - 2)

    # 创建一个函数, 用于计算斐波那契数列, 该函数会将每一次调用的结果缓存起来, 避免再次调用重复计算
    @lru_cache(maxsize=100)
    def fib_cacheable(n: int) -> int:
        if n < 2:
            return n
        return fib_cacheable(n - 1) + fib_cacheable(n - 2)

    # 计算斐波那契数列并记录函数调用的时间
    start = time.perf_counter()
    assert fib_nocache(30) == 832040
    assert time.perf_counter() - start > 0.01

    # 计算斐波那契数列并记录函数调用的时间
    start = time.perf_counter()
    assert fib_cacheable(30) == 832040
    assert time.perf_counter() - start < 0.01

    # 获取函数上的缓存数据
    cache_info = fib_cacheable.cache_info()

    # 确认缓存命中次数
    assert cache_info.hits == 28
    # 确认缓存未命中次数
    assert cache_info.misses == 31
    # 确认缓存的最大数量, `None` 表示无上限, 这里的值为 100, 为设置缓存时设置的缓存最大数量
    assert cache_info.maxsize == 100
    # 确认缓存的当前数量
    assert cache_info.currsize == 31

    # 清理 `fib_cacheable` 函数上的缓存
    fib_cacheable.cache_clear()

    # 重新计算斐波那契数列
    assert fib_cacheable(31) == 1346269


def test_lru_cache_decorator_on_method() -> None:
    """测试 `@lru_cache` 装饰器用于对象方法

    `@lru_cache` 装饰器也是用于缓存函数调用结果, 以避免函数重复计算, `@lru_cache` 表示缓存具备淘汰策略,
    可以在缓存数量达到最大值时, 淘汰最久未使用的缓存项

    当一个方法被 `@lru_cache` 装饰器修饰后, 则该函数上会增加几个方法, 分别为:
    - `cache_clear` 方法: 用于清除该函数上的缓存
    - `cache_info` 属性: 用于获取该函数的缓存信息
    - `cache_parameters` 方法: 用于获取创建缓存时, 所设置的缓存参数

    本例中, `Fib` 类具备两个方法, 一个不加缓存, 导致所需时间比较久; 一个通过 `@lru_cache` 装饰器缓存函数的结果,
    以避免重复计算, 计算效率较高
    """

    class Fib:
        """斐波那契数列类"""

        def nocache(self, n: int) -> int:
            """计算斐波那契数列

            Args:
                n (`int`): 斐波那契数列的索引

            Returns:
                `int`: 斐波那契数列的值
            """
            if n < 2:
                return n
            return self.nocache(n - 1) + self.nocache(n - 2)

        @lru_cache(maxsize=100)
        def cacheable(self, n: int) -> int:
            """计算斐波那契数列

            该函数通过 `@lru_cache` 装饰器缓存函数的结果, 避免重复计算, 计算效率较高

            Args:
                n (`int`): 斐波那契数列的索引

            Returns:
                `int`: 斐波那契数列的值
            """
            if n < 2:
                return n
            return self.cacheable(n - 1) + self.cacheable(n - 2)

    fib = Fib()

    # 计算斐波那契数列并记录函数调用的时间
    start = time.perf_counter()
    assert fib.nocache(30) == 832040
    assert time.perf_counter() - start > 0.01

    # 计算斐波那契数列并记录函数调用的时间
    start = time.perf_counter()
    assert fib.cacheable(30) == 832040
    assert time.perf_counter() - start < 0.01

    # 获取函数上的缓存数据
    cache_info = fib.cacheable.cache_info()

    # 确认缓存命中次数
    assert cache_info.hits == 28
    # 确认缓存未命中次数
    assert cache_info.misses == 31
    # 确认缓存的最大数量, `None` 表示无上限, 这里的值为 100, 为设置缓存时设置的缓存最大数量
    assert cache_info.maxsize == 100
    # 确认缓存的当前数量
    assert cache_info.currsize == 31

    # 清理 `fib_cacheable` 函数上的缓存
    fib.cacheable.cache_clear()

    # 重新计算斐波那契数列
    assert fib.cacheable(31) == 1346269


def test_cached_property_decorator() -> None:
    """用于对对象的属性值进行缓存

    Python 的类可以通过 `@property` 装饰器将类中的一个方法定义为 “属性”， 属性值即为方法的返回值

    可以通过 `@cached_property` 装饰器将属性值进行缓存，避免重复计算属性值, 从而提高性能

    当缓存过期后, 可通过 `del` 关键字删除被缓存的属性, 实际上是删除缓存
    """

    class Fib:
        """定义类, 用于测试 `@cached_property` 装饰器, 对属性值进行缓存"""

        def __init__(self, n: int) -> None:
            self._n = n

        @staticmethod
        def _calculate_fib(n: int) -> int:
            """计算 `n` 的斐波那契数"""
            if n < 2:
                return n
            return Fib._calculate_fib(n - 1) + Fib._calculate_fib(n - 2)

        @cached_property
        def result(self) -> int:
            """获取当前对象属性 `_n` 的斐波那契值

            该属性使用 `cached_property` 装饰器修饰，因此 `result` 属性只会计算一次
            """
            return Fib._calculate_fib(self._n)

        def clear_cache(self) -> None:
            """清除属性上的缓存"""
            del self.result

        @property
        def n(self) -> int:
            """获取当前对象属性 `_n` 的值"""
            return self._n

        @n.setter
        def n(self, n: int) -> None:
            """设置当前对象属性 `_n` 的值"""
            self._n = n
            del self.result

    # 创建对象
    fib = Fib(30)

    # 获取属性值并记录属性值计算所需时间
    start = time.perf_counter()
    assert fib.result == 832040
    assert time.perf_counter() - start > 0.01

    # 获取属性值并记录属性值计算所需时间, 因为有缓存, 所以计算时间可忽略不计
    start = time.perf_counter()
    assert fib.result == 832040
    assert time.perf_counter() - start < 0.01

    # 修改属性值, 则 n 属性的 setter 方法会触发清除 result 属性的缓存
    fib.n = 31

    # 重新获取属性值, 确认之前的缓存已经失效
    start = time.perf_counter()
    assert fib.result == 1346269
    assert time.perf_counter() - start > 0.01

    # 再次获取属性值, 由于属性值已被缓存, 故属性值计算时间已忽略不计
    start = time.perf_counter()
    assert fib.result == 1346269
    assert time.perf_counter() - start < 0.01


def test_singledispatch_decorator() -> None:
    """测试 `@singledispatch` 装饰器创建单一分发函数

    `@singledispatch` 装饰器用于创建一个函数, 该函数会根据参数的类型进行分发处理, 并返回相应的结果

    通过 `@singledispatch` 装饰器创建的函数, 一方面可以避免在函数中使用大量条件分支, 造成代码复杂; 另一方面,
    可以按需注册不同参数类型的处理函数, 避免不同类型参数的处理逻辑相互冲突

    `@singledispatch` 装饰器起到的作用有些类似其它语言的函数重载, 通过不同的参数类型进行分发处理, 返回相应的结果,
    但注意: `@singledispatch` 装饰器只允许后续处理函数改变默认处理函数的参数类型, 不允许改变参数个数和参数顺序
    """

    # 定义默认处理函数以及不同参数类型的处理函数, 当调用函数时所给的参数类型与指定的某个分发函数一致时, 将由该函数负责处理调用,
    # 否则由默认函数处理调用

    @singledispatch
    def format_value(value: Any) -> str:
        """定义默认处理函数, 用于处理所有参数类型

        Args:
            `value` (`Any`): 参数值, 可以为任意类型

        Returns:
            `str`: 格式化后的参数值, 字符串类型
        """
        return str(value)

    @format_value.register(bool)
    def _(value: bool) -> str:
        """当以针对于布尔类型参数时的处理函数

        Args:
            `value` (`bool`): 布尔类型参数值

        Returns:
            `str`: 格式化后的布尔值, 字符串类型
        """
        return "true" if value else "false"

    @format_value.register(dict)
    def _(value: dict[str, Any]) -> str:
        """格式化字典值

        Args:
            value (`dict`): 字典值

        Returns:
            `str`: 格式化后的字典值
        """
        return json.dumps(value)

    # 确认参数为整型时, 默认处理函数将处理该参数
    assert format_value(123) == "123"

    # 确认参数为布尔类型时, 将由对应的处理函数处理该参数
    assert format_value(True) == "true"

    # 确认参数为字典类型时, 将由对应的处理函数处理该参数
    assert format_value({"a": 1, "b": 2}) == '{"a": 1, "b": 2}'


def test_singledispatch_decorator_on_method() -> None:
    """通过 `@singledispatchmethod` 装饰器为类的普通方法创建单一分发方法

    `@singledispatchmethod` 和 `@singledispatch` 装饰器作用基本相同, 区别在于:

    - `@singledispatchmethod` 装饰器不能修饰函数, 但可以修饰类中的方法, 包括普通方法, 类方法, 静态方法
    - `@singledispatch` 则只能修饰函数, 不能修饰类中的方法
    """

    class Formatter:
        """定义类, 用于测试 `@singledispatchmethod` 装饰器在类的普通方法上创建单一分发方法"""

        @singledispatchmethod
        def format(self, data: Any) -> str:
            """用于默认的格式化参数, 可以对任意 `data` 参数进行格式化"""
            return str(data)

        @format.register(bool)
        def _(self, data: bool) -> str:
            """用于 `data` 参数为布尔参数的格式化"""
            return "true" if data else "false"

        @format.register(dict)
        def _(self, data: dict[str, Any]) -> str:
            """用于 `data` 参数为字典参数的格式化"""
            return json.dumps(data)

    # 创建 `Formatter` 类的实例对象, 并调用 `format` 方法
    fmt = Formatter()

    # 确认参数为整型时, 默认处理函数将处理该参数
    assert fmt.format(123) == "123"

    # 确认参数为布尔类型时, 将由对应的处理函数处理该参数
    assert fmt.format(True) == "true"

    # 确认参数为字典类型时, 将由对应的处理函数处理该参数
    assert fmt.format({"a": 1, "b": 2}) == '{"a": 1, "b": 2}'


def test_singledispatch_decorator_on_class_method() -> None:
    """通过 `@singledispatchmethod` 装饰器为类的类方法创建单一分发方法"""

    class Formatter:
        """定义类, 用于测试 `@singledispatchmethod` 装饰器在类方法上创建单一分发方法"""

        @singledispatchmethod
        @classmethod
        def format(cls, data: Any) -> str:
            """用于默认的格式化参数, 可以对任意 `data` 参数进行格式化"""
            return str(data)

        @format.register(bool)
        @classmethod
        def _(cls, data: bool) -> str:
            """用于 `data` 参数为布尔参数的格式化"""
            return "true" if data else "false"

        @format.register(dict)
        @classmethod
        def _(cls, data: dict[str, Any]) -> str:
            """用于 `data` 参数为字典参数的格式化"""
            return json.dumps(data)

    # 确认参数为整型时, 默认处理函数将处理该参数
    assert Formatter.format(123) == "123"

    # 确认参数为布尔类型时, 将由对应的处理函数处理该参数
    assert Formatter.format(True) == "true"

    # 确认参数为字典类型时, 将由对应的处理函数处理该参数
    assert Formatter.format({"a": 1, "b": 2}) == '{"a": 1, "b": 2}'


def test_singledispatch_decorator_on_static_method() -> None:
    """通过 `@singledispatchmethod` 装饰器为类的静态方法创建单一分发方法"""

    class Formatter:
        """定义类, 用于测试 `@singledispatchmethod` 装饰器在类静态上创建单一分发方法"""

        @singledispatchmethod
        @staticmethod
        def format(data: Any) -> str:
            """用于默认的格式化参数, 可以对任意 `data` 参数进行格式化"""
            return str(data)

        @format.register(bool)
        @staticmethod
        def _(data: bool) -> str:
            """用于 `data` 参数为布尔参数的格式化"""
            return "true" if data else "false"

        @format.register(dict)
        @staticmethod
        def _(data: dict[str, Any]) -> str:
            """用于 `data` 参数为字典参数的格式化"""
            return json.dumps(data)

    # 确认参数为整型时, 默认处理函数将处理该参数
    assert Formatter.format(123) == "123"

    # 确认参数为布尔类型时, 将由对应的处理函数处理该参数
    assert Formatter.format(True) == "true"

    # 确认参数为字典类型时, 将由对应的处理函数处理该参数
    assert Formatter.format({"a": 1, "b": 2}) == '{"a": 1, "b": 2}'


def test_wraps_decorator() -> None:
    """测试 `@wraps` 装饰器

    `@wraps` 装饰器用于将一个函数的元信息复制到另一个函数中, 使得被装饰的函数的元信息保持不变, 避免被装饰函数的元信息被修改

    例如:

    ```python
    # 定义一个装饰器, 该装饰器会传入被装饰函数 (`fn` 参数), 并返回 `wrapper` 函数以取代被装饰函数
    # 当调用被装饰函数时， 实际调用的是 `wrapper` 函数, 在 `wrapped` 函数内部调用被装饰函数 (`fn`)
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        # 这里使用 `wraps` 装饰器将 `fn` 的元信息复制到 `wrapper` 函数中, 以防止在获取被装饰函数元信息时,
        # 返回 `wrapped` 函数的元信息
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return fn(*args, **kwargs)

        return wrapper

    # 定义一个被装饰的函数, 通过 `@decorator` 装饰器装饰
    @decorator
    def some_fn(value: Any) -> str:
        return ""

    # 输出被装饰函数 (`some_fn`) 的名称 (函数元信息之一), 返回的就是 `some_fn` 的元信息, 而非 `wrapper` 函数的元信息
    print(some_fn.__name__)
    ```
    """

    def origin_fn(arg1: int, arg2: str) -> None:
        """定义一个函数, 作为被包装函数"""
        pass

    @wraps(origin_fn)
    def wrapped_fn(value: Any) -> str:
        """定义一个被包装函数, 该函数的元信息会通过 `@wraps` 装饰器被 `origin_fn` 函数元信息取代"""
        return ""

    # 确认 `wrapped_fn` 的元信息被 `origin_fn` 的元信息取代
    assert wrapped_fn.__name__ == "origin_fn"

    # 确认 `wrapped_fn` 函数被 `origin_fn` 函数包装
    assert wrapped_fn.__wrapped__ == origin_fn

    # 确认 `wrapped_fn` 函数的参数信息仍为其实际定义的参数信息, 没有被 `origin_fn` 函数的参数信息取代
    args = inspect.getfullargspec(wrapped_fn)
    assert args.args == ["value"]


def test_update_wraps_function() -> None:
    """测试 `update_wrapper` 函数

    `update_wrapper` 函数的作用和 `wraps` 装饰器类似, 都是用于将一个函数的元信息复制到另一个函数中, 避免被装饰函数的元信息被修改,
    只是 `update_wrapper` 是通过函数参数的方式将元信息复制到另一个函数中, 而 `wraps` 是通过装饰器的方式将元信息复制到另一个函数中

    另外, `update_wrapper` 函数的功能更为强大, 可以指定要复制的元信息列表和要更新的元信息列表

    `update_wrapper` 函数的参数如下:
    - `wrapper`: 被装饰的函数
    - `wrapped`: 被装饰函数的源函数
    - `assigned`: 要复制的元信息列表, 默认为 `('__module__', '__name__', '__qualname__', '__doc__', '__annotations__')`
    - `updated`: 要更新的元信息列表, 默认为 `('__dict__',)`

    也就是说, `update_wrapper` 函数将第二个参数所引用函数的元信息复制到第一个参数所引用的函数中,
    并且可以指定要复制的元信息列表和要更新的元信息列表

    例如:

    ```python
    # 定义一个装饰器, 该装饰器会传入被装饰函数 (`fn` 参数), 并返回 `wrapper` 函数以取代被装饰函数
    # 当调用被装饰函数时， 实际调用的是 `wrapper` 函数, 在 `wrapped` 函数内部调用被装饰函数 (`fn`)
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return fn(*args, **kwargs)

        # 这里将 `fn` 函数的元信息复制到 `wrapper` 函数中
        update_wrapper(wrapper, fn)
        return wrapper

    # 定义一个被装饰的函数, 通过 `@decorator` 装饰器装饰
    @decorator
    def some_fn(value: Any) -> str:
        return ""

    # 输出被装饰函数 (`some_fn`) 的名称 (函数元信息之一), 返回的就是 `some_fn` 的元信息, 而非 `wrapper` 函数的元信息
    print(some_fn.__name__)
    ```
    """

    def origin_fn(arg1: int, arg2: str) -> None:
        """定义一个函数, 作为被包装函数"""
        pass

    def wrapped_fn(value: Any) -> str:
        """定义一个被包装函数, 该函数的元信息会通过 `@wraps` 装饰器被 `origin_fn` 函数元信息取代"""
        return ""

    # 将 `origin_fn` 函数的元信息复制到 `wrapped_fn` 函数中
    update_wrapper(wrapped_fn, origin_fn)

    # 确认 `wrapped_fn` 的元信息被 `origin_fn` 的元信息取代
    assert wrapped_fn.__name__ == "origin_fn"

    # 确认 `wrapped_fn` 函数的参数信息仍为其实际定义的参数信息, 没有被 `origin_fn` 函数的参数信息取代
    args = inspect.getfullargspec(wrapped_fn)
    assert args.args == ["value"]


def test_total_order_decorator() -> None:
    """测试 `@total_order` 装饰器

    通过 `@total_order` 装饰器可以将一个类装饰为可进行比较的类, 使得该类对象可以进行比较运算, 并且比较运算的结果是可预测的

    如果一个类添加了 `@total_ordering` 装饰器, 则该类只要具备 `__eq__` 方法和其它比较方法中的一个 (例如 `__lt__` 方法),
    则其它比较方法都会自动进行添加, 包括:
    - `__ne__` 方法: 即 `!=` 运算符重载
    - `__lt__` 方法: 即 `<` 运算符重载
    - `__le__` 方法: 即 `<=` 运算符重载
    - `__gt__` 方法: 即 `>` 运算符重载
    - `__ge__` 方法: 即 `>=` 运算符重载
    """

    @total_ordering
    class Point:
        """定义一个类, 用于测试 `total_order` 装饰器"""

        def __init__(self, x: float, y: float) -> None:
            self.x = x
            self.y = y

        def __eq__(self, o: Any) -> bool:
            """定义 `==` 比较运算符"""
            if not isinstance(o, Point):
                raise TypeError("Cannot compare Point with non-Point")

            return self.x == o.x and self.y == o.y

        def __lt__(self, o: Self) -> bool:
            """定义 `<` 比较运算符"""
            return (self.x, self.y) < (o.x, o.y)

    # 创建两个对象
    p1, p2 = Point(1, 2), Point(3, 4)

    # 确认对象的所有比较运算符都具备, 且结果可预测
    assert not p1 == p2
    assert p1 != p2
    assert p1 < p2
    assert p1 <= p2  # type: ignore[operator]
    assert not p1 > p2
    assert not p1 >= p2  # type: ignore[operator]
