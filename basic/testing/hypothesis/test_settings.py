import time
from datetime import timedelta
from typing import Callable, List, Sequence

import pytest
from hypothesis import HealthCheck, Verbosity, given, settings
from hypothesis import strategies as st

_examples = []


@settings(max_examples=50)
@given(n=st.integers(min_value=1, max_value=10))
def test_hypothesis_settings(n: int) -> None:
    """
    设置假设用例的配置, 不同的配置会对假设的测试用例数量, 范围以及测试本身产生不同的影响

    ```
    class hypothesis.settings(
        parent=None,
        *,
        max_examples=not_set, # 整数, 默认值 100, 设置每个测试的用例上限
        derandomize=not_set,  # 布尔值, 默认值 False, 如果为 True, 则用例不再随机
        database=not_set,
        verbosity=not_set, # 枚举, 默认值 Verbosity.normal, 控制消息的详细度
        phases=not_set,
        stateful_step_count=not_set,  #
        report_multiple_bugs=not_set, # 布尔值, 默认为 True, 是否同时报告多个测试失
                                      # 败, 如果为 False, 则一旦测试失败, 整个测试
                                      # 停止
        suppress_health_check=not_set, # 列表, 默认为空列表, 列表包含需要禁用的
                                       # HealthCheck 对象
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
@pytest.mark.skip(reason="该测试一定会失败")
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


def _data_generator(count: int, delay=10) -> Sequence[str]:
    """
    生成假设值的函数, 该函数在会人为产生一些延迟, 该延迟会导致健康检查失败

    Args:
        count (int): 要产生的列表长度
        delay (int, optional): 该函数执行延迟的时间. Defaults to `10`.

    Returns:
        Sequence[str]: 假设的列表对象
    """
    # 休眠指定时间, 从而产生延迟
    time.sleep(delay)

    # 返回假设用例
    return [str(n) for n in range(1, count + 1)]


@pytest.mark.skip(reason="执行过慢, 禁止该测试执行")
@settings(
    max_examples=3,
    suppress_health_check=[HealthCheck.too_slow],
)
@given(ss=st.builds(  # 通过 builds 方法假设用例, 即用例通过 _data_generator 函数产生
    _data_generator,
    count=st.integers(  # 传递给 _data_generator 函数的 count 参数
        min_value=1,
        max_value=5,
    ),
))
def test_disable_health_check(ss: Sequence[str]) -> None:
    """
    Health Check (健康检查) 是一套检查假设执行是否正确的机制, 如果健康检查失败, 则测试会
    因为抛出 `FailedHealthCheck` 异常而被打断

    `@settings` 装饰器的 `suppress_health_check` 参数可以设置禁用那些健康检查的项目,
    以保证在特殊情况下, 测试得以正常执行

    可以禁用的健康检查项在 `hypothesis.HealthCheck` 枚举中定义, 定义的检查项包括:

    - `data_too_large`: 检查是否因为假设产生的数据过大, 从而阻碍了太多的测试用例无法执行.
                        这个检查项不是依据假设值对象大小来计算的, 例如在已生成的对象中选
                        中一个 `100MB` 的对象和从头开始生成一个 `10KB` 的对象两种情况,
                        后者才会引发检查失败
    - `filter_too_much`: 检查在产生假设用例时, 是否过滤掉了太多的用例
    - `too_slow`: 产生假设用例时消耗了过多时间
    - `return_value`: 检查测试函数是否返回了非 `None` 值, 通常这是没有必要的
    - `large_base_example`: 检查执行 shrink 操作的原始测试用例是否过大, 这通常意味着产
                            生原始假设用例的策略不对
    - `not_a_test_method`: 检查 `@given` 装饰器是否用在了非测试函数上
    - `function_scoped_fixture`: 检查 `@given` 注解是否用在了具备 `@fixture` 注解
                                 (scope 为 `function` 的情况下) 的函数上, 这样会导
                                 致 `fixture` 为每个假设用例执行一次, 这通常不符合预
                                 期

    本例中演示了一个产生测试用例非常缓慢的场景, 如果不通过 `suppress_health_check` 禁止
    掉 `HealthCheck.too_slow` 项, 则会引发健康检查失败, 从而结束测试
    """
    # 确认参数为列表集合类型
    assert isinstance(ss, List)

    # 确认列表元素项为字符串类型
    for s in ss:
        assert isinstance(s, str)


def test_settings_object() -> None:
    """
    如何创建各类 `settings` 对象

    - 默认的 `settings` 对象, 即不使用 `@settings` 装饰器时默认使用的 `settings` 对象
    - 可以通过 `settings` 类型创建自定义的对象, 通过 `@settings` 装饰器设置
    - 如果已有 `settings` 对象, 则可以在其基础上派生一个新对象
    """
    # 获取默认的 settings 对象
    default_s: settings = settings.default
    # 确认默认设置的参数
    assert default_s.max_examples == 100
    assert default_s.deadline == timedelta(milliseconds=200)

    # 自定义 settings 对象, 自定义对象会自动从默认 settings 对象派生
    parent_s = settings(deadline=timedelta(milliseconds=500))
    # 确认未设置值的项遵守默认 settings 对象的对应值
    assert parent_s.max_examples == 100
    # 确认已设置值的项
    assert parent_s.deadline == timedelta(milliseconds=500)

    # 从已有的 settings 对象派生新的 settings 对象
    child_s = settings(parent_s, max_examples=200)
    # 确认未设置值的项从父 settings 对象继承
    assert child_s.max_examples == 200
    # 确认以设置值的项
    assert child_s.deadline == timedelta(milliseconds=500)


def test_use_profile() -> None:
    """
    `settings.register_profile` 方法可以注册一个命名的配置信息, 并在之后进行获取和使用,
    其定义如下:

    ```python
    static settings.register_profile(
        name,        # 配置文件的名称
        parent=None, # 要继承的父配置对象
        **kwargs     # 要修改的配置项, 未设置的保持其默认值
    )
    ```

    获取配置文件的方式有两种:
    - `settings.get_profile(name)` 获取之前注册的配置文件, 返回一个 `settings` 对象,
      为之前注册的配置信息
    - `settings.load_profile(name)` 读取之前注册的配置文件, 将会覆盖默认的配置信息, 之
      后通过 `settings()` 实例化的对象, 其内容为注册的配置信息

    另外的使用方式包括:
    在测试命令行中指定要使用的配置文件名称, 当前需要提前注册对应的配置文件 (例如在
    `conftest.py` 文件中进行注册)

    ```bash
    pytest tests --hypothesis-profile <profile-name>
    ```
    """
    # 注册一个配置文件, 为其中的某些设置项做出更改
    settings.register_profile("p1", max_examples=1000)

    # 读取默认的设置信息
    s = settings()
    # 确认配置项为默认值
    assert s.max_examples == 100

    # 获取注册名为 p1 的配置信息, 返回 settings 对象
    s = settings.get_profile("p1")
    # 确认配置项为修改后的值
    assert s.max_examples == 1000

    # 重新确认默认的配置信息未被更改
    s = settings()
    assert s.max_examples == 100

    # 读取配置文件, 此时默认配置信息会被修改为 p1 中的内容
    settings.load_profile("p1")

    # 在此读取默认的配置信息, 确认配置项已不是默认值
    s = settings()
    assert s.max_examples == 1000


def teardown_function(fn: Callable) -> None:
    """
    测试结束后, 验证最终结果
    """
    if fn == test_hypothesis_settings:
        # 检测 max_examples 设置是否生效, 确认用例被执行的次数
        assert 1 <= len(_examples) <= 50
