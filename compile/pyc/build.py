import glob
import os
import py_compile
import shutil
import sys
from dataclasses import dataclass, field
from itertools import chain
from os import path
from typing import Dict, Set

_SRC_DIR = "src"
_CUR_DIR = path.dirname(__file__)
_BUILD_IGNORE = ".buildignore"
_DIST_DIR = "dist"

class File:
    def __init__(self, filename: str) -> None:
        self._filename = filename
        self._to_compile = filename.endswith(".py")

    def __repr__(self) -> str:
        return self._filename

    @staticmethod
    def _create_base_path(filename: str) -> str:
        base = path.dirname(filename)
        if not path.exists(base):
            os.makedirs(base)

        return filename

    def _make_compile_dist(self) -> str:
        base, _ = path.splitext(self._filename)
        base = base.removeprefix(f"{_SRC_DIR}/")
        dist = self._create_base_path(path.join(_DIST_DIR, f"{base}.pyc"))

        print(f"{self._filename:30} => {dist}")
        return dist

    def _make_copy_dist(self) -> str:
        return self._create_base_path(
            path.join(_CUR_DIR, _DIST_DIR, self._filename.removeprefix(f"{_SRC_DIR}/"))
        )

    def _do_compile(self) -> None:
        py_compile.compile(
            self._filename,
            cfile=self._make_compile_dist(),
            doraise=True,
            optimize=2,
            quiet=1,
        )

    def _do_copy(self) -> None:
        shutil.copyfile(
            self._filename,
            self._make_copy_dist(),
            follow_symlinks=False,
        )

    def build(self) -> None:
        """
        生成目标文件
        """
        if self._to_compile:
            self._do_compile()
        else:
            self._do_copy()


def _collect_ignore_files() -> Set[str]:
    def fix(name: str) -> str:
        if name and (name.startswith("/") or name.startswith("\\")):
            name = name[1:]

        if name and (name.endswith("/") or name.endswith("\\")):
            name = name[0:-1]

        return name

    def read_build_ignore() -> Set[str]:
        if not path.exists(_BUILD_IGNORE):
            return set()

        with open(_BUILD_IGNORE, encoding="utf8") as fp:
            return set(
                filter(
                    lambda l: len(l) > 0,
                    (fix(s.strip()) for s in fp.readlines()),
                )
            )

    return set(
        chain(
            *[
                glob.glob(
                    pattern, root_dir=_CUR_DIR, recursive=True, include_hidden=True
                )
                for pattern in read_build_ignore()
            ]
        )
    )


def _error(err: str) -> None:
    print(f"ERR: {err}")
    sys.exit(-1)


@dataclass
class CommandArgs:
    cmd: str = field(default="")
    args: Dict[str, str] = field(default_factory=lambda: {})


def build_pyc() -> None:
    ignore_files = _collect_ignore_files()
    ignore_files.add(_BUILD_IGNORE)

    for root, dirs, files in os.walk(_SRC_DIR):
        if root in ignore_files:
            dirs[:] = []
            continue

        for file in files:
            file = path.join(root, file).removeprefix("./")
            if file not in ignore_files:
                File(file).build()


if __name__ == "__main__":
    build_pyc()
