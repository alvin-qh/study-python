from pytest import fail, mark


@mark.xfail
def test_xfail_pass():
    """
    `@xfail` 装饰器用于标记一个 *可能会失败* 的测试, 无论测试成功或失败, 都不会影响整个测试的执行
    - 如果测试通过, 则在测试报告中记录 `xpass`
    - 如果测试失败, 则在测试报告中记录 `xfailed`
    """


@mark.xfail
def test_xfail_failed():
    """
    `@xfail` 装饰器与测试失败的情况
    """
    fail()
