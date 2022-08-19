from typing import Callable

from hypothesis import given, settings
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
        max_examples=not_set,
        derandomize=not_set,
        database=not_set,
        verbosity=not_set,
        phases=not_set,
        stateful_step_count=not_set,
        report_multiple_bugs=not_set,
        suppress_health_check=not_set,
        deadline=not_set,
        print_blob=not_set
    )
    ```
    """
    # 确认设置生效
    assert settings().max_examples == 50

    # 确认假设数据的范围
    assert 1 <= n <= 10

    # 追加假设的数据, 用于在 teardown_function 中判断设置是否生效
    _examples.append(n)


def teardown_function(fn: Callable) -> None:
    """
    """
    if fn == test_hypothesis_settings:
        assert 1 <= len(_examples) <= 50
