import time
from typing import List, Sequence, Tuple

import hypothesis.strategies as st
from hypothesis.internal.conjecture.data import ConjectureData


class User:
    """定义一个类型用于对其对象进行假设操作"""

    def __init__(self, name: str) -> None:
        """初始化对象

        Args:
            - `name` (`str`): name 参数
        """
        self._name = name

    @property
    def name(self) -> str:
        """获取 `name` 属性

        Returns:
            `str`: `name` 属性值
        """
        return self._name


class UserStrategy(st.SearchStrategy[User]):
    """用于生成 `User` 对象的假设类型"""

    def __init__(self, name: st.SearchStrategy[str]) -> None:
        """初始化 `User` 对象假设类型

        Args:
            - `name` (`st.SearchStrategy[str]`): 产生 `name` 属性的假设对象
        """
        super().__init__()  # type: ignore[no-untyped-call]
        self._name = name

    def do_draw(self, data: ConjectureData) -> User:
        """执行假设操作, 产生一个 `User` 类型对象

        Args:
            - `data` (`ConjectureData`): 假设库数据数据, 参见 Hypothesis example database

        Returns:
            `User`: 产生的 `User` 类型测试用例
        """
        # 通过 _name 假设对象为 User 类型生成 name 属性
        return User(self._name.do_draw(data))

    def __repr__(self) -> str:
        return f"User(name={self._name})"


# 注册类型
st.register_type_strategy(
    User, UserStrategy(name=st.from_regex(r"[A-Z][a-z]{3,5}", fullmatch=True))
)


@st.composite
def list_and_index(
    draw: st.DrawFn,
    elements: st.SearchStrategy[int] = st.integers(),
) -> Tuple[List[int], int]:
    """定义一个组合的假设函数, 可以根据所给参数组合多个假设对象生成用例数据

    Args:
        - `draw` (`st.DrawFn`): 根据假设对象产生用例的函数
        - `elements` (`SearchStrategy[E]`, optional): 产生类型为 `E` 用例的假设对象. Defaults to `st.integers()`.

    Returns:
        `Tuple[List[int], int]`: 产生的假设值
    """
    # 产生一个集合类型的用例
    xs = draw(st.lists(elements, min_size=1))

    # 产生集合下标范围内的任意整数
    i = draw(st.integers(min_value=0, max_value=len(xs) - 1))

    # 返回用例值
    return (xs, i)


@st.composite
def element_and_index[E](
    draw: st.DrawFn,
    element: st.SearchStrategy[E],
) -> Tuple[int, E]:
    """利用 `@composite` 装饰器产生一个假设组合, 其定义如下:

    ```
    # 装饰器修饰的函数, f 参数类型为 Callable[[DrawFn, SearchStrategy], Any]
    hypothesis.strategies.composite(f)
    ```

    Args:
        - `draw` (`st.DrawFn`): 产生指定假设的函数
        - `element` (`st.SearchStrategy[E]`): 产生假设的 `Strategy` 类

    Returns:
        `Tuple[int, E]`: 输出的假设值
    """
    # 根据传入的假设类型产生假设值
    elem = draw(element)

    # 产生一个整数假设值
    index = draw(st.integers(min_value=1, max_value=1000))

    # 返回假设值组合
    return (index, elem)


def delay_data_generator(count: int, delay: int = 10) -> Sequence[str]:
    """生成假设值的函数, 该函数在会人为产生一些延迟, 该延迟会导致健康检查失败

    Args:
        - `count` (`int`): 要产生的列表长度
        - `delay` (`int`, optional): 该函数执行延迟的时间. Defaults to `10`.

    Returns:
        `Sequence[str]`: 假设的列表对象
    """
    # 休眠指定时间, 从而产生延迟
    time.sleep(delay)

    # 返回假设用例
    return [str(n) for n in range(1, count + 1)]
