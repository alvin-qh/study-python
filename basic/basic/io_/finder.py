import os
from fnmatch import fnmatch
from typing import Iterator


def find_all_files(
    path_: str,
    pattern: str = "*",
    single_level: bool = False,
    yield_folders: bool = False,
) -> Iterator[str]:
    """查找指定路径下的所有内容

    Args:
        - `path_` (`str`): 要访问的路径 (相对路径/绝对路径)
        - `pattern` (`str`, optional): 要匹配的模式, 可包含通配符. 多个模式使用 `;` 隔开. Defaults to `*`.
        - `single_level` (`bool`, optional): 是否只遍历第一层. Defaults to False.
        - `yield_folders` (`bool`, optional): 在遍历结果中是否包含文件夹. Defaults to False.

    Yields:
        `Iterator[str]`: 文件内容迭代
    """
    patterns = pattern.split(";")

    # 对指定路径进行遍历, 返回一个三元组的列表:
    #   root: 正在遍历的路径本身
    #   dirs: 正在遍历的路径所包含的子路径列表
    #   files: 正在遍历的路径所包含的文件列表
    for root, dirs, files in os.walk(
        path_,  # 要遍历的路径
        topdown=False,  # 遍历顺序
        followlinks=False,  # 是否获取连接指向的原文件
        onerror=lambda e: e,  # 出错后处理函数
    ):
        # 如果要包含文件夹, 则将文件夹列表合并到结果中
        if yield_folders:
            files.extend(dirs)

        # 过滤当前路径下包含的所有文件
        for name in files:
            for pattern in patterns:
                if fnmatch(name, pattern):
                    yield os.path.join(root, name)
                    break

        if single_level:
            break
