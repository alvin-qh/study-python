from multiprocessing import cpu_count

from .group import ProcessGroup
from .prime import PrimeResult, prime_to_dict, prime_to_list, prime_to_result

# 可以启动的进程总数
N_PROCESSES = cpu_count()

__all__ = [
    "N_PROCESSES",
    "prime_to_list",
    "prime_to_dict",
    "PrimeResult",
    "prime_to_result",
    "ProcessGroup",
]
