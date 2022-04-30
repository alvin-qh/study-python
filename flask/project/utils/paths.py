import glob
import os
import pkgutil
import sys
from typing import List, Set, Tuple, Union

from flask import Flask


def _is_file_valid(file: str) -> bool:
    """
    判断文件名是否有效

    Args:
        file (str): 文件的路径名称
    """
    file = os.path.basename(file)
    return file != "." and not (file.startswith("__") and file.endswith("__"))


StrCollection = Union[List[str], Tuple[str], Set[str]]


def list_all_files(paths: StrCollection, patterns: StrCollection, recursive: bool = False) -> List[str]:
    """
    列举路径下所有文件

    Args:
        paths (Union[List[str], Tuple[str], Set[str]]): 文件路径集合
        patterns (Union[List[str], Tuple[str], Set[str]]): 列举文件的模式（glob 标准）
        recursive (bool, optional): 是否递归子目录. Defaults to False.
    """
    if not isinstance(paths, (list, tuple, set)):
        paths = [paths]

    if not isinstance(patterns, (list, tuple, set)):
        patterns = [patterns]

    files = set()
    # 遍历所有的路径和模式
    for path in paths:
        for pattern in patterns:
            # 将某个路径和某个模式对应
            pattern = os.path.join(path, pattern)
            # 通过 glob 函数列举所有的子文件
            files.update({f for f in glob.glob(
                pattern, recursive=recursive) if _is_file_valid(f)})

    return list(files)


def get_module_path(module_name: str) -> str:
    """
    获取一个 python 模块的路径

    Args:
        module_name (str): 模块名称
    """
    # 获取模块的 loader
    loader = pkgutil.get_loader(module_name)

    # 获取模块的文件名
    if hasattr(loader, "get_filename"):
        filename = loader.get_filename(module_name)
    elif hasattr(loader, "archive"):
        filename = loader.archive
    else:
        __import__(module_name)
        filename = sys.modules[module_name].__file__

    # 获取模块文件名的绝对路径
    return os.path.abspath(os.path.dirname(filename))


# 默认监控的文件名称
DEFAULT_WATCH_FILE_TYPES = (
    "py", "html", "js", "jsx", "ts", "vue", "less", "css")


def watch_files_for_develop(app: Flask, types: Tuple[str] = DEFAULT_WATCH_FILE_TYPES):
    """
    获取检测文件的列表（用于开发模式）

    Args:
        app (Flask): Flask 实例对象
        types (Tuple[str], optional): 用于监控的文件类型列表. Defaults to DEFAULT_WATCH_FILE_TYPES.
    """
    if not app.debug:
        return None

    # 获取模块的路径
    package_path = get_module_path(app.import_name)
    # 要监控的路径范围
    paths = (package_path, app.template_folder, app.static_folder)
    # 要监控的文件模式
    patterns = {os.path.join("**", f"*.{t}") for t in types}

    # 获取监控文件列表
    return list_all_files(paths, patterns, recursive=True)
