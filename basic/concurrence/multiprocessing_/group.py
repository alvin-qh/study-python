from multiprocessing import Process
from typing import Any, Callable, Iterable

# 参数列表类型
ArgList = Iterable[Iterable[Any]] | None


class ProcessGroup:
    """
    进程组类, 表示一组进程
    """

    def __init__(
        self, target: Callable, arglist: ArgList = None, count=0
    ) -> None:
        """
        构造器, 构造一个进程组对象

        Args:
            target (Callable): 进程入口函数
            arglist (ArgList, optional): 进程参数组, 每组参数为一个 Tuple, 表示传给进程入口函数的参数.
            Defaults to None.
            count (int, optional): 进程的个数. Defaults to 0.
        """
        if count:
            # 如果传递了 count 参数, 则按数量产生进程
            self._ps = [Process(target=target) for _ in range(count)]
        elif arglist:
            # 否则按传入参数列表的个数实产生进程
            self._ps = [
                Process(target=target, args=args) for args in arglist
            ]
            count = len(self._ps)

        # 保存进程数
        self._count = count

    def __len__(self) -> int:
        return self._count

    def start(self) -> None:
        """
        启动所有进程
        """
        # 启动所以进程
        for p in self._ps:
            p.start()

    def join(self) -> None:
        """
        等待所有进程结束
        """
        # 等待进程执行完毕
        for p in self._ps:
            p.join()

    def start_and_join(self) -> None:
        """
        启动所有进程并等待所有进程结束
        """
        self.start()
        self.join()
