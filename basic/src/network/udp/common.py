from typing import Tuple


def format_addr(addr: Tuple[str, int]) -> str:
    """将网络地址转化为字符串"""
    return f"{addr[0]}:{addr[1]}"
