from dataclasses import dataclass
from functools import cache, cmp_to_key, partial, reduce
from operator import add
from typing import Self
import time


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
    """测试 `cache` 装饰器用于函数

    `cache` 装饰器用于缓存函数的结果, 以避免重复计算

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


def test_cache_decorator_on_method() -> None:
    """测试 `cache` 装饰器用于对象方法

    `cache` 装饰器用于缓存函数的结果, 以避免重复计算

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
