from typing import Iterator


class PrimeResult:
    """
    演示在 `Manager` 对象中注册自定义类型
    """

    def __init__(self) -> None:
        """
        构造器, 实例化存储结果的列表对象
        """
        self._l = []

    def put(self, n: int, r: bool) -> None:
        """
        存储一个结果

        Args:
            n (int): 数字
            r (bool): 数字是否质数的结果
        """
        self._l.append((n, r))

    def iterator(self) -> Iterator:
        """
        获取结果集合的迭代器对象

        Returns:
            Iterator: 结果集合的迭代器对象
        """
        return iter(self._l)
