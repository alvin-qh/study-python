import glob
import os
import pkgutil
import sys
from typing import Iterable, List, Tuple, Union

from flask import Flask


def _is_file_valid(pathname: str) -> bool:
    """判断文件名是否有效

    Args:
        - `pathname` (`str`): 文件路径名称

    Returns:
        `bool`: `True` 表示文件存在
    """
    file = os.path.basename(pathname)
    return file != "." and not (file.startswith("__") and file.endswith("__"))


def list_all_files(
    paths: Union[str, Iterable[str]],
    patterns: Union[str, Iterable[str]],
    recursive: bool = False,
) -> List[str]:
    """列举路径下所有文件

    Args:
        - `paths` (`Union[str, Iterable[str]]`): 路径集合
        - `patterns` (`Union[str, Iterable[str]]`): 文件名匹配模式
        - `recursive` (`bool`, optional): 是否递归查找. Defaults to `False`.

    Returns:
        `List[str]`: 符合查找条件的文件集合
    """
    if isinstance(paths, str):
        paths = [paths]

    if isinstance(patterns, str):
        patterns = [patterns]

    files = set()

    # 遍历所有的路径和模式
    for path in paths:
        if not path:
            continue

        for pattern in patterns:
            # 将某个路径和某个模式对应
            pattern = os.path.join(path, pattern)
            # 通过 glob 函数列举所有的子文件
            files.update(
                {
                    file
                    for file in glob.glob(pattern, recursive=recursive)
                    if _is_file_valid(file)
                }
            )

    return list(files)


def get_module_path(module_name: str) -> str:
    """获取一个 Python 模块的路径

    Args:
        - `module_name` (`str`): 模块名称

    Returns:
        `str`: 模块路径名称
    """
    # 获取模块的 loader
    loader = pkgutil.get_loader(module_name)

    # 获取模块的文件名
    if hasattr(loader, "get_filename"):
        filename = loader.get_filename(module_name)  # type: ignore
    elif hasattr(loader, "archive"):
        filename = loader.archive  # type: ignore
    else:
        __import__(module_name)
        filename = sys.modules[module_name].__file__

    if not filename:
        raise ModuleNotFoundError(module_name)

    # 获取模块文件名的绝对路径
    return str(os.path.abspath(os.path.dirname(filename)))


# 默认监控的文件名称
_DEFAULT_WATCH_FILE_TYPES = (
    "py",
    "html",
    "js",
    "jsx",
    "ts",
    "vue",
    "less",
    "css",
)


def get_watch_files_for_develop(
    app: Flask, types: Tuple[str, ...] = _DEFAULT_WATCH_FILE_TYPES
) -> List[str]:
    """获取检测文件的列表（用于开发模式）

    Args:
        app (Flask): Flask 实例对象
        types (Tuple[str], optional): 用于监控的文件类型列表. Defaults to DEFAULT_WATCH_FILE_TYPES.
    """
    if not app.debug:
        return []

    # 获取模块的路径
    package_path = get_module_path(app.import_name)

    # 要监控的路径范围
    paths = [
        str(package_path),
        str(app.template_folder or ""),
        str(app.static_folder or ""),
    ]

    # 要监控的文件模式
    patterns = {os.path.join("**", f"*.{type_}") for type_ in types}

    # 获取监控文件列表
    return list_all_files(paths, patterns, recursive=True)
