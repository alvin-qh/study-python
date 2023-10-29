import re
from typing import Callable, cast

from hypothesis import assume, event, example, given, note
from hypothesis import strategies as st
from hypothesis import target

# 基于属性的自动化测试 (Property-based testing)
#
# 是指编写对你的代码来说为真的逻辑语句 (即"属性"), 然后使用自动化工具来生成测试输入 (一般来
# 说，是指某种特定类型的随机生成输入数据)，并观察程序接受该输入时属性是否保持不变。如果某个输
# 入违反了某一条属性，则用户证明程序存在一处错误，并找到一个能够演示该错误的便捷示例


@given(x=st.integers(), y=st.integers())
def test_given(x: int, y: int) -> None:
    """
    本例演示了如何使用 `@given` 装饰器, 该装饰器定义如下:

    ```
    hypothesis.given(
        *_given_arguments,  # 要假设的参数, 按测试函数的参数位置设置
        **_given_kwargs     # 要假设的参数, 按测试函数的参数名称设置
    )
    ```

    `@given` 装饰器用于提供一组 "假设", 该组假设中包含了指定类型的随机数据 (包括边界数据),
    以这组数据为驱动, 驱动测试执行

    `@given(x=st.integers(), y=st.integers())` 表示会给测试函数 `x`, `y` 两个参数,
    整数类型

    本例中还是用到了 `note` 函数, 定义如下:

    ```
    hypothesis.note(value)
    ```

    该函数类似 `print` 函数, 用于输出参数值, 但 `note` 函数仅在测试失败时显示输出
    """
    # 当测试失败时, 在标准输出打印指定内容
    note(f"given x={x}, y={y}")


expected_str = set()


@given(s=st.text())
@example(s="alvin")
@example(s="emma")
def test_example_decorator(s: str) -> None:
    """
    本例演示了 `@example` 装饰器, 定义如下:

    ```
    hypothesis.example(
        *args,      # 要确定的参数, 按测试函数的参数位置设置
        **kwargs    # 要确定的参数, 按测试函数的参数名称设置
    )
    ```

    `@example` 装饰器用于指定必须产生的测试参数值, 无论设置的
    参数值是否已被假设, 其都必然通过参数传递给测试
    """
    # 当测试失败时, 在标准输出打印指定内容
    note(f"given s={s}")

    # 过滤字符串
    if re.match("^[\x01-\x7F]{1,}$", s):
        # 当测试失败时, 在标准输出打印指定内容
        note(f"filtered s={s}")

        # 确认字符串的所有字符都有 ASCII 字符组成
        for c in cast(str, s):
            assert 0 < ord(c) < 128

    if s in {"alvin", "emma"}:
        # 将指定测试用例值加到确认列表中
        expected_str.add(s)


def test_example_output() -> None:
    """
    通过 `example()` 方法获取测试用例

    本例中获取 `10` 个测试用例
    """
    examples = [
        st.integers(min_value=0, max_value=10).example()
        for _ in range(10)
    ]
    assert len(examples) == 10
    assert all(0 <= n <= 10 for n in examples)


@given(s=st.text(
    alphabet=(  # 字符串由 A-Za-z 字符组成
        [chr(c) for c in range(ord("a"), ord("z"))] +
        [chr(c) for c in range(ord("A"), ord("Z"))]
    )
))
def test_assume(s: str) -> None:
    """
    排除无效的参数

    `assume(condition)` 函数会在当条件为 `False` 时, 跳过当前测试, 这样可以忽略
    一些不满足要求的假设, 让测试可以按最初的设计正常执行
    """
    # 跳过 s 为 None 或 空字符串 的情况
    assume(s)

    # 因为 assume(s) 的作用, s 为 None 及空字符串的测试已被停止, 所以不会触发断言
    # 若去掉 assume(s) 函数调用, 则会引发断言
    assert len(s) > 0


@given(n=st.integers().filter(lambda x: x % 2 == 0))
def test_event_output(n: int) -> None:
    """
    输出事件信息, 以便对假设用例的产生做更进一步的说明.
    要查看详细的测试用例产生日志, 需要在测试启动命令行上加入
    `--hypothesis-show-statistics` 参数

    本例中执行 `pytest testing/hypothesis/test_core.py::test_event --hypothesis-show-statistics`
    命令行后, 可以看到如下输出:

    ``` # noqa
    testing/hypothesis/test_core.py::test_event:

    - during reuse phase (0.00 seconds):
      - Typical runtimes: < 1ms, ~ 40% in data generation
      - 1 passing examples, 0 failing examples, 0 invalid examples

    - during generate phase (0.09 seconds):
      - Typical runtimes: < 1ms, ~ 56% in data generation
      - 99 passing examples, 0 failing examples, 18 invalid examples
      - Events:
        * 51.28%, Retried draw from integers().filter(lambda x: x % 2 == 0) to satisfy filter
        * 35.04%, n % 3 == 0
        * 26.50%, n % 3 == 2
        * 23.08%, n % 3 == 1
        * 15.38%, Aborted test because unable to satisfy integers().filter(lambda x: x % 2 == 0)

    - Stopped because settings.max_examples=100
    ```
    """
    event(f"n % 3 == {n % 3}")


@given(n=st.integers(min_value=-100, max_value=100))
def test_hypothesis_target(n: int) -> None:
    """ # noqa
    target 方法可以对一个目标结果进行观察, 目标结果是一个 `int` 或 `float` 类型值, 可以
    表示任意指标

    指标值可以为
    — 集合中的元素或队列中的任务数
    - 任务的平均运行时间或最大运行时间 (如果使用 `label` 参数，则两者皆可)
    - 数据的压缩比 (可能是每个算法或每个级别)
    - 状态机执行的步骤数

    可选的 `label` 参数可以用来区分. 因此分别优化不同的观察结果，比如:
    数据集的平均值和标准差

    通过如下命令执行测试, 可以看到指标的统计结果

    ```
    pytest testing/hypothesis/test_core.py::test_hypothesis_target --hypothesis-show-statistics
    ```
    """
    if n < 0:
        target(n, label="negative")
    elif n > 0:
        target(n, label="positive")


def teardown_function(fn: Callable) -> None:
    """
    测试结束后验证整体结果
    """
    if fn == test_example_decorator:
        # 确认 test_example 中指定的测试用例被执行
        assert expected_str == {"alvin", "emma"}
