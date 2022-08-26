import hypothesis.strategies as st
from hypothesis.internal.conjecture.data import ConjectureData


class User:
    """
    定义一个类型用于对其对象进行假设操作
    """

    def __init__(self, name: str) -> None:
        """
        初始化对象

        Args:
            name (str): name 参数
        """
        self._name = name

    @property
    def name(self) -> str:
        """
        获取 `name` 属性

        Returns:
            str: `name` 属性值
        """
        return self._name


class UserStrategy(st.SearchStrategy):
    """
    用于生成 `User` 对象的假设类型
    """

    def __init__(self, name: st.SearchStrategy[str]):
        """
        初始化 `User` 对象假设类型

        Args:
            name (st.SearchStrategy[str]): 产生 `name` 属性的假设对象
        """
        self._name = name

    def do_draw(self, data: ConjectureData) -> User:
        """
        执行假设操作, 产生一个 `User` 类型对象

        Args:
            data (ConjectureData): 假设库数据数据, 参见 Hypothesis example database

        Returns:
            User: 产生的 `User` 类型测试用例
        """
        # 通过 _name 假设对象为 User 类型生成 name 属性
        return User(self._name.do_draw(data))

    def __repr__(self) -> str:
        return f"User(name={self._name})"


# 注册类型
st.register_type_strategy(
    User,
    UserStrategy(name=st.from_regex(r"[A-Z][a-z]{3,5}", fullmatch=True))
)
