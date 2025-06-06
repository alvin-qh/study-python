from pytest import mark

from basic.testing import Counter

counter = Counter()
repeat = Counter()


@mark.flaky(reruns=5, reruns_delay=1)
def test_rerun() -> None:
    """
    通过安装 `pytest-rerunfailures` 插件 (`pip install pytest-rerunfailures`),
    可以为失败的测试设置重试次数

    参数 `reruns=5`, 即测试失败最多重试 `5` 次

    参数 `reruns_delay=1`, 即每次重试间隔 `1` 秒

    由于 `assert counter.value == 5` 这条语句, 所以该测试的前 `4` 次执行都是失败的,
    最后一次执行会成功, 整体算成功

    注意:
        - 不可以和 `@fixture` 装饰器一起使用
        - 该插件与 `pytest-xdist` 的 `--looponfail` 标志不兼容
        - 该插件与核心 `--pdb` 标志不兼容
    """
    # 增加调用次数记录
    counter.increase()

    # 验证一共调用 5 次
    assert counter.value <= 6


@mark.repeat(3)
def test_repeating() -> None:
    """
    通过安装 `pytest-repeat` 插件 (`pip install pytest-repeat`), 可以设置测试重复运行的次数
    """
    # 重复执行记录加 1
    repeat.increase()


def teardown_module() -> None:
    """
    测试模块结束时执行
    """
    # test_rerun 函数执行 5 次
    assert counter.value <= 6

    # test_repeating 函数执行 3 次
    assert repeat.value == 3
