import os
import time
import timeit
from types import TracebackType
from typing import IO, Optional, Type

from portalocker import LockFlags, LockException
from portalocker import lock as file_lock
from portalocker import unlock as file_unlock


class FileLock:
    """文件锁类型

    本类型演示如何使用文件锁. 文件锁可以用于跨进程甚至跨程序的锁. 原理是在磁盘上建立一个文件, 并通过操作系统对文件进行锁定的功能
    """

    _DEFAULT_CHECK_INTERVAL = 0.25

    # 锁文件名模板
    _lock_file_template = ".{}.lock"

    def __init__(self, name: str) -> None:
        """初始化锁对象

        Args:
            - `name` (`str`): 锁的名称, 也会作为锁文件的名称定义

        Raises:
            `ValueError`: 锁名称无效
        """
        if not name:
            raise ValueError("invalid name")

        # 格式化锁文件名
        self._filename = self._lock_file_template.format(name)
        # 文件描述符
        self._fd: IO[bytes] | None = None
        # 是否锁定
        self._locked = False

    def acquire(self, timeout: float = 5.0) -> bool:
        """加锁

        如果锁已经被占用则进入阻塞等待, 直到锁被释放

        Args:
            - `blocking` (`bool`, optional): 是否阻塞. Defaults to `False`.

        Returns:
            `bool`: 加锁成功返回 `True`
        """
        # 创建锁文件, 得到文件描述符
        fd = open(self._filename, "+wb")
        start = timeit.default_timer()
        while True:
            try:
                # 对文件进行加锁操作
                file_lock(fd, LockFlags.EXCLUSIVE | LockFlags.NON_BLOCKING)
                self._fd = fd
                break
            except LockException:
                if timeit.default_timer() - start > timeout:
                    return False

                time.sleep(self._DEFAULT_CHECK_INTERVAL)

        return True

    def release(self) -> None:
        """解锁"""
        if self._fd:
            fd = self._fd
            self._fd = None
            if fd:
                file_unlock(fd)
                fd.close()

        try:
            os.remove(self._filename)
        except Exception:
            pass

    # 定义 __enter__ 方法
    __enter__ = acquire

    def __exit__(
        self,
        exc_type: Optional[Type[Exception]],
        exc_value: Optional[Exception],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.release()
