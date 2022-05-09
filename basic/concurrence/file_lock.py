import fcntl
import os
from threading import get_ident


class FileLock:
    """
    文件锁类型
    """
    # 锁文件名模板
    _lock_file_template = ".{}.lock"

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
        # 文件描述符
        self._fd = 0
        # 是否锁定
        self._locked = False

    def acquire(self, blocking=True) -> bool:
        """
        加锁

        如果锁已经被占用则进入阻塞等待, 直到锁被释放

        Args:
            blocking (bool, optional): 是否阻塞. Defaults to False.

        Returns:
            bool: 加锁成功返回 True
        """
        # 创建锁文件, 得到文件描述符
        fd = os.open(self._filename, os.O_RDONLY | os.O_CREAT)

        # 文件锁标识
        opt = fcntl.LOCK_EX
        if not blocking:
            # 非阻塞标识
            opt |= fcntl.LOCK_NB

        try:
            # 对文件进行加锁操作
            fcntl.flock(fd, opt)
            # 保存文件描述符
            self._fd = fd

            # 返回加锁成功
            return True
        except Exception:
            # 返回加锁失败
            return False

    # 定义 __enter__ 方法
    __enter__ = acquire

    def release(self) -> None:
        """
        解锁
        """
        fd = self._fd
        if fd:
            fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)

            self._fd = None

        try:
            os.remove(self._filename)
        except Exception:
            pass

    def __exit__(self, t, v, tb) -> None:
        self.release()
