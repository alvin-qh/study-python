import fcntl
import os
from typing import Optional

FileDescriptor = int


class FileLock:
    """
    文件锁类型
    """
    # 锁文件名模板
    _lock_file_template = "{}.lock"

    class _Lock:
        """
        锁上下文类型
        """

        def __init__(self, fd: FileDescriptor) -> None:
            """
            初始化锁上下文对象

            Args:
                fd (FileDescriptor): 锁相关联的文件描述符对象
            """
            self._fd = fd

        def __enter__(self) -> None:
            """
            进入锁上下文
            """
            pass

        def __exit__(self, exc_type, exc_val, exc_tb) -> None:
            """
            退出锁上下文
            """
            if self._fd:
                # 解除锁定
                fcntl.flock(self._fd, fcntl.LOCK_UN)
                # 清理文件描述符对象, 令锁无效
                self._fd = None

    def __init__(self, name: str) -> None:
        """
        初始化锁对象

        Args:
            name (str): 锁的名称, 也会作为锁文件的名称定义

        Raises:
            ValueError: 锁名称无效
        """
        if not name:
            raise ValueError("invalid name")

        # 格式化锁文件名
        self._filename = self._lock_file_template.format(name)

    def lock(self) -> _Lock:
        """
        加锁
        如果锁已经被占用则进入阻塞等待, 直到锁被释放

        Returns:
            _Lock: 锁上下文对象
        """
        # 创建锁文件, 得到文件描述符
        fd = os.open(self._filename, os.O_RDONLY | os.O_CREAT)

        # 对文件进行加锁操作
        fcntl.flock(fd, fcntl.LOCK_EX)
        # 返回锁上下文对象
        return self._Lock(fd)

    def try_lock(self) -> Optional[_Lock]:
        """
        尝试加锁
        如果锁已经被占用则返回 None

        Returns:
            Optional[_Lock]: 如果加锁成功则返回锁上下文对象, 否则返回 None
        """
        # 创建锁文件, 得到文件描述符
        fd = os.open(self._filename, os.O_RDONLY | os.O_CREAT)
        try:
            # 对文件进行加锁操作, LOCK_NB 表示不阻塞
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return self._Lock(fd)
        except BlockingIOError:
            # 如果抛出 BlockingIOError, 表示锁已被占用, 返回 None 值
            return None

    def remove(self) -> None:
        """
        删除锁文件
        """
        try:
            os.remove(self._filename)
        except Exception:
            pass
