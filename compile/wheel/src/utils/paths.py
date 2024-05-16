import glob
import os
import pkgutil
import sys
from typing import Iterable, List, Optional, Tuple, Union

from flask import Flask


def _is_file_valid(file: str) -> bool:
    file = os.path.basename(file)
    return file != "." and not (file.startswith("__") and file.endswith("__"))


def list_all_files(
    paths: Iterable[Optional[Union[str, os.PathLike[str]]]],
    patterns: Iterable[str],
    recursive: bool = False,
) -> List[str]:
    files = set()
    for path in paths:
        if not path:
            continue

        for pattern in patterns:
            pattern = os.path.join(path, pattern)
            files.update(
                {
                    f
                    for f in glob.glob(pattern, recursive=recursive)
                    if _is_file_valid(f)
                }
            )

    return list(files)


def get_module_path(module_name: str) -> str:
    loader = pkgutil.get_loader(module_name)

    if hasattr(loader, "get_filename"):
        filename = loader.get_filename(module_name)  # type: ignore
    elif hasattr(loader, "archive"):
        filename = loader.archive  # type: ignore
    else:
        __import__(module_name)
        filename = sys.modules[module_name].__file__

    if not filename:
        raise ModuleNotFoundError(module_name)

    return str(os.path.abspath(os.path.dirname(filename)))


DEFAULT_WATCH_FILE_TYPES = ("py", "html", "js", "jsx", "ts", "vue", "less", "css")


def watch_files_for_develop(
    app: Flask,
    types: Tuple[str, ...] = DEFAULT_WATCH_FILE_TYPES,
) -> Optional[List[str]]:
    if not app.debug:
        return None

    package_path = get_module_path(app.import_name)
    paths = [package_path, app.template_folder, app.static_folder]

    patterns = {os.path.join("**", f"*.{t}") for t in types}
    return list_all_files(paths, patterns, recursive=True)
