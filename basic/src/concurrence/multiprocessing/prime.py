from typing import Dict, Iterator, List, Tuple


def prime_to_list(n: int, result: List[Tuple[int, bool]]) -> None:
    """
    进程入口函数, 用于演示 `Manager` 类型的 `list` 方法产生的列表对象

    Args:
        n (int): 整数
        result (List[Tuple[int, bool]]): 保存结果的共享列表对象
    """
    if n <= 1:
        # 将结果存入列表
        result.append((n, False))
        return

    for i in range(2, n):
        if n % i == 0:
            # 将结果存入列表
            result.append((n, False))
            return

    # 将结果存入列表
    result.append((n, True))


def prime_to_dict(n: int, result: Dict[int, bool]) -> None:
    """
    进程入口函数, 用于演示 `Manager` 类型的 `dict` 方法产生的字典对象

    Args:
        n (int): 整数
        result (Dict[int, bool]): 保存结果的共享字典对象
    """
    if n <= 1:
        # 将结果存入字典
        result[n] = False
        return

    for i in range(2, n):
        if n % i == 0:
            # 将结果存入字典
            result[n] = False
            return

    # 将结果存入字典
    result[n] = True


class PrimeResult:
    """
    演示在 `Manager` 对象中注册自定义类型
    """

    _l: List[Tuple[int, bool]]

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

    def iterator(self) -> Iterator[Tuple[int, bool]]:
        """
        获取结果集合的迭代器对象

        Returns:
            Iterator: 结果集合的迭代器对象
        """
        return iter(self._l)


def prime_to_result(n: int, result: PrimeResult) -> None:
    """
    进程入口函数, 用于演示通过 `BaseManager` 类型的 `register` 方法注册的类型

    Args:
        n (int): 整数
        result (PrimeResult): PrimeResult 类型的代理对象
    """
    if n <= 1:
        # 保存结果
        result.put(n, False)
        return

    for i in range(2, n):
        if n % i == 0:
            # 保存结果
            result.put(n, False)
            return

    # 保存结果
    result.put(n, True)
