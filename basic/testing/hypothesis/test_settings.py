from typing import Callable, List

import pytest
from hypothesis import Verbosity, given, settings
from hypothesis import strategies as st

_examples = []


@settings(max_examples=50)
@given(n=st.integers(min_value=1, max_value=10))
def test_hypothesis_settings(n: int) -> None:
    """

    ```
    class hypothesis.settings(
        parent=None,
        *,
        max_examples=not_set, # 整数, 默认值 100, 设置每个测试的用例上限
        derandomize=not_set,  # 布尔值, 默认值 False, 如果为 True, 则用例不再随机
        database=not_set,
        verbosity=not_set, # 枚举, 默认值 Verbosity.normal, 控制消息的详细度
        phases=not_set,
        stateful_step_count=not_set,
        report_multiple_bugs=not_set,
        suppress_health_check=not_set,
        deadline=not_set, # timedelta 对象, 设置每次测试的限定时长, 超过这个限定则
                          # 测试失败
        print_blob=not_set # 布尔值, 默认为 False, 测试失败后, 输出测试用例的记录索引,
                           # 以复现该错误
    )
    ```
    """
    # 确认设置生效
    assert settings().max_examples == 50

    # 确认假设数据的范围
    assert 1 <= n <= 10

    # 追加假设的数据, 用于在 teardown_function 中判断设置是否生效
    _examples.append(n)


@settings(verbosity=Verbosity.verbose)
@given(lst=st.lists(
    elements=st.integers(min_value=1, max_value=10), min_size=1),
)
def test_intermediate_result(lst: List[int]) -> None:
    """
    输出更为详细的测试用例执行情况

    `@settings(verbosity=Verbosity.verbose)` 输出测试函数和每个假设的参数值
    """
    assert any(lst)


# cspell: disable
@pytest.mark.skip  # 该测试一定会失败, 所以标记为 skip, 需要时取消即可
@settings(print_blob=True)
@given(v=st.floats())
# @reproduce_failure('6.54.2', b'ACABAP/4AAAAAAAA')
def test_print_blob(v: float) -> None:
    """
    输出数据库中记录的失败记录索引, 并重新执行相同的用例

    通过标记 `@settings(print_blob=True)`, 当测试失败后, 输出对应测试用例的记录索引,
    根据提示, 通过类似 `@reproduce_failure('6.54.2', b'ACABAP/4AAAAAAAA')` 的标记,
    即可重新执行一次失败用例
    """
    # 当 v = nan 时引发断言, nan 无法进行比较
    assert v == v

# cspell: enable


def teardown_function(fn: Callable) -> None:
    """
    测试结束后, 验证最终结果
    """
    if fn == test_hypothesis_settings:
        # 检测 max_examples 设置是否生效, 确认用例被执行的次数
        assert 1 <= len(_examples) <= 50
