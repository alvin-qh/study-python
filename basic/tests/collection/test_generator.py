from typing import Generator, Iterator


def test_yield_to_create_generator() -> None:
    """测试 `yield` 关键字

    `yield` 用于返回一个 `Generator` 类型的对象, 接收方可以通过该对象获取函数内生成的结果
    """

    def xrange(min_: int, max_: int, step: int = 1) -> Iterator[int]:
        """产生一个从最小值到 (最大值 - 1) 范围内的结果序列

        Args:
            - `min_` (`int`): 最小值
            - `max_` (`int`): 最大值
            - `step` (`int`, optional): 增长的步长. Defaults to `1`.

        Yields:
            `Iterator[int]`: 生成器对象, 相当于 `Generator[int, None, None]` 类型
        """
        while min_ < max_:
            yield min_
            min_ += step

    it = list(xrange(1, 10))
    assert it == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    it = list(xrange(1, 10, step=2))
    assert it == [1, 3, 5, 7, 9]


def test_echo_round() -> None:
    """测试带回复交互的 `Generator` 对象"""

    def echo_round() -> Generator[int, float, str]:
        """返回一个 `Generator` 对象, 包含三个部分的值

        Returns:
            - `str`: 返回生成器对象

        Yields:
            `Generator[int, float, str]`: 完整的 `Generator` 对象定义, 包含三部分的值, 分别为：
            - Iterate Type: `int` 类型, 即返回的迭代器包含的值类型
            - Send Type: `float` 类型, 即要发送调用方的值类型
            - Return Type: `str` 类型, 即调用方结束数据生成后返回的值
        """
        # 获取 send 值, 即外部通过 Generator 对象发送的值
        # yield 0 表示对 Generator 的第一个值是 0
        # 也可以不关注该值, 例如 send = yield 即可
        sent = yield 0

        # 判断通过 Generator 对象发送的值不为负数
        while sent >= 0:
            # 对发送回来的值进行四舍五入
            sent = yield round(sent)

        # 返回终止 Generator 迭代的值
        return "Done"

    # 调用函数, 获取 Generator 对象
    g = echo_round()
    # 第一次迭代, 返回 yield 0 语句的值
    assert next(g) == 0

    # 发送数据到调用方, 调用方会进行四舍五入后返回整数值
    assert g.send(1.1) == 1

    # 发送数据到调用方, 调用方会进行四舍五入后返回整数值
    assert g.send(2.1) == 2

    # 发送数据到调用方, 调用方会进行四舍五入后返回整数值
    assert g.send(0) == 0

    try:
        # 发送数据 -1 会导致调用方结束, 此时调用方返回 Done 字符串, 作为迭代结束的结果
        g.send(-1)
    except StopIteration as e:
        # 从迭代结束异常重获取结果
        assert str(e) == "Done"
