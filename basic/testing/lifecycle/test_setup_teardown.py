import sys
from types import ModuleType
from typing import Callable


class Counter:
    """
    计数器类
    """

    def __init__(self) -> None:
        """
        初始化计数器
        """
        self._value = 0

    def increase(self) -> None:
        """
        计数器加 1
        """
        self._value += 1

    @property
    def value(self) -> int:
        """
        获取计数器总计数值

        Returns:
            int: 计数器总计数值
        """
        return self._value


class Step:
    """
    记录步骤的累
    """

    def __init__(self) -> None:
        """
        初始化步骤状态
        """
        self._state = ""

    def start(self) -> None:
        """
        将状态设置为 start
        """
        self._state = "start"

    def finish(self) -> None:
        """
        将状态设置为 finish
        """
        self._state = "finish"

    @property
    def state(self) -> str:
        """
        获取当前状态

        Returns:
            str: 当前状态
        """
        return self._state


# 记录 setup_function 函数调用次数
setup_function_counter = Counter()

# 记录 teardown_function 函数调用次数
teardown_function_counter = Counter()

# 记录模块执行步骤
module_step = Step()


def setup_module(module: ModuleType) -> None:
    """
    函数在模块开始前执行一次

    Args:
        module (ModuleType): 当前测试的模块对象
    """
    assert module == sys.modules[__name__]
    module_step.start()


def teardown_module(module: ModuleType) -> None:
    """
    函数在模块结束后执行一次

    Args:
        module (ModuleType): 当前测试的模块对象
    """
    # 验证 module 为当前模块的对象
    assert module == sys.modules[__name__]

    # 验证执行步骤此时为 start
    assert module_step.state == "start"

    # 标记执行步骤为 finish
    module_step.finish()

    # 验证 setup_function 和 teardown_function 此时均调用两次
    assert setup_function_counter.value == teardown_function_counter.value == 2


def setup_function(func: Callable) -> None:
    """
    在每个测试函数执行开始前执行一次

    Args:
        func (Callable): 执行的测试函数
    """
    # 验证传入的测试函数对象
    assert func in {test_one, test_two}

    # 标记 setup_function 调用次数加 1
    setup_function_counter.increase()


def teardown_function(func: Callable) -> None:
    """
    在每个测试函数执行结束后执行一次

    Args:
        func (Callable): 执行的测试函数
    """
    # 验证传入的测试函数对象
    assert func in {test_one, test_two}

    # 验证 teardown_function 比 setup_function 此时少调用一次
    assert teardown_function_counter.value == setup_function_counter.value - 1

    # 标记 teardown_function 调用次数加 1
    teardown_function_counter.increase()


def test_one() -> None:
    """
    执行第一个测试函数
    """


def test_two() -> None:
    """
    执行第二个测试函数
    """


class TestCase:
    """
    测试类
    """

    # 记录 setup_class 方法调用次数
    setup_class_counter = Counter()

    # 记录 teardown_class 方法调用次数
    teardown_class_counter = Counter()

    # 记录 setup_method 方法调用次数
    setup_method_counter = Counter()

    # 记录 teardown_method 方法调用次数
    teardown_method_counter = Counter()

    # 记录测试类的执行步骤
    class_step = Step()

    # 记录测试方法的执行步骤
    method_step = Step()

    @classmethod
    def setup_class(cls) -> None:
        """
        测试类开始前执行一次
        """
        # 标记测试类执行步骤为 start
        cls.class_step.start()
        # 记录 setup_class 调用次数加 1
        cls.setup_class_counter.increase()

    @classmethod
    def teardown_class(cls) -> None:
        """
        测试类结束后执行一次
        """
        # 验证测试类执行步骤为 start
        assert cls.class_step.state == "start"

        # 标记测试类执行步骤为 finish
        cls.class_step.finish()

        # 验证 teardown_class 方法比 setup_class 此时少调用一次
        assert cls.teardown_class_counter.value == cls.setup_class_counter.value - 1 == 0

        # 验证 setup_method 和 teardown_method 此时均调用两次
        assert cls.setup_method_counter.value == cls.teardown_method_counter.value == 2

        # 记录 teardown_class 调用次数加 1
        cls.teardown_class_counter.increase()

    def setup_method(self, method: Callable) -> None:
        """
        类中每个测试方法执行前执行一次

        Args:
            method (Callable): 要执行的测试方法对象
        """
        # 验证传入的测试方法对象
        assert method in {self.test_three, self.test_four}

        # 设置测试方法执行步骤为 start
        self.method_step.start()

        # 设置 setup_method 方法调用次数加 1
        self.setup_method_counter.increase()

    def teardown_method(self, method: Callable) -> None:
        """
        类中每个测试方法结束后执行一次

        Args:
            method (Callable): 要执行的测试方法对象
        """

        # 验证传入的测试方法对象
        assert method in {self.test_three, self.test_four}

        # 验证测试方法步骤此时为 start
        assert self.method_step.state == "start"

        # 标记测试方法步骤为 finish
        self.method_step.finish()

        # 验证 teardown_method 方法比 setup_method 此时少调用一次
        assert self.teardown_method_counter.value == self.setup_method_counter.value - 1

        # 标记 teardown_method 方法执行次数加 1
        self.teardown_method_counter.increase()

    def test_three(self) -> None:
        """
        第一个测试方法
        """

    def test_four(self) -> None:
        """
        第二个测试方法
        """
