# 可以启动的进程总数
from multiprocessing import cpu_count

N_THREADS = cpu_count()

__all__ = [
    "N_THREADS",
]
