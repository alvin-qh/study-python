from multiprocessing import cpu_count

# 可以启动的进程总数
N_PROCESSES = cpu_count()

__all__ = [
    "N_PROCESSES",
]
