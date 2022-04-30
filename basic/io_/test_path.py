import os
import shutil
from fnmatch import fnmatch
from typing import Iterator

from pytest import raises


def test_join_function() -> None:
    """
    将多个路径拼合成一个完整路径
    """
    p1 = "a/b/c/d"
    p2 = "x/y"
    p3 = "test.txt"

    # 拼合路径
    p = os.path.join(p1, p2, p3)
    assert p == "a/b/c/d/x/y/test.txt"


def test_split_function() -> None:
    """
    将路径分割为 目录 和 文件名
    """
    p = os.path.split("/usr/local/bin/vim")

    # 返回结果第 1 项为目录, 第 2 项为文件名
    assert p == ("/usr/local/bin", "vim")


def test_abspath_function() -> None:
    """
    获取相对路径对应的绝对路径
    """
    # 获取指定相对路径的绝对路径
    p = os.path.abspath("./io_/test_path.py")

    # 判断绝对路径是否正确
    assert p.endswith("/basic/io_/test_path.py")


def test_listdir_function() -> None:
    """
    列举目录下面的内容, 包含文件和子路径
    """
    # 列举 io_ 目录下的所有内容
    items = os.listdir("./io_")

    assert len(items) > 0
    # 判断 test_path.py 在路径包含的内容中
    assert "test_path.py" in items


def test_isdir_isfile_function() -> None:
    """
    判断指定的路径表示 目录 还是 文件
    """
    # 当前路径下的 io_ 是一个子路径
    assert os.path.isdir("io_") is True

    # 当前路径下的 requirements.txt 是一个文件
    assert os.path.isfile("requirements.txt") is True


PATH_1 = "a"
PATH_2 = "b"
PATHS = "a/b/c"


def teardown_function() -> None:
    """
    当每个测试结束后执行
    """
    for dir in [PATH_1, PATH_2]:
        shutil.rmtree(dir, ignore_errors=True)


def test_dir_operates() -> None:
    """
    创建和删除路径
    """
    # 创建路径
    os.mkdir(PATH_1)
    # 判断指定路径已存在
    assert os.path.exists(PATH_1) is True
    assert os.path.isdir(PATH_1) is True

    # 删除路径
    os.rmdir(PATH_1)
    # 判断指定路径不存在
    assert os.path.exists(PATH_1) is False
    assert os.path.isdir(PATH_1) is False


def test_dirs_operates() -> None:
    """
    创建和删除深层次路径
    """
    # 创建路径
    os.makedirs(PATHS, mode=0o777, exist_ok=True)
    # 判断指定路径已存在
    assert os.path.exists(PATHS) is True
    assert os.path.isdir(PATHS) is True

    # 删除路径
    os.removedirs(PATHS)
    # 判断指定路径不存在
    assert os.path.exists(PATHS) is False
    assert os.path.isdir(PATHS) is False


def test_splitext_function() -> None:
    """
    将一个文件名分为两部分: (文件名, 扩展名)
    """
    r = os.path.splitext("~/Music/Hello.mp3")

    # 获取文件名部分
    assert r[0] == "~/Music/Hello"
    # 获取扩展名部分
    assert r[1] == ".mp3"


def test_fnmatch_function() -> None:
    """
    判断一个文件名是否和所给的相符

    可以使用通配符匹配文件名
    """
    # 列举 io_ 目录下的所有内容
    for fn in os.listdir("./io_"):
        # 排除掉路径部分
        if os.path.isdir(fn):
            continue

        # 确认文件匹配 *.py 通配符
        assert fnmatch(fn, "*.py") is True


def find_all_files(
    path_: str,
    pattern="*",
    single_level=False,
    yield_folders=False,
) -> Iterator[str]:
    """
    查找指定路径下的所有内容

    Args:
        path_ (str): 要访问的路径 (相对路径/绝对路径)
        pattern (str, optional): 要匹配的模式, 可包含通配符. 多个模式使用 `;` 隔开.
        Defaults to "*".
        single_level (bool, optional): 是否只遍历第一层. Defaults to False.
        yield_folders (bool, optional): 在遍历结果中是否包含文件夹. Defaults to False.

    Yields:
        Iterator[str]: _description_
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


def test_find_all_files() -> None:
    """
    测试 find_all_files 函数
    """
    # 获取 io_ 路径下匹配 *.py 的文件
    files = find_all_files("io_", "*.py")
    assert set(files) == {
        "io_/__init__.py",
        "io_/crc64.py",
        "io_/test_file.py",
        "io_/test_path.py",
        'io_/test_byte.py',
        'io_/test_compress.py',
        'io_/test_asyncio.py',
        'io_/test_pickle.py',
    }


def touch(path_: str, filenames: Iterator[str]) -> None:
    """
    创建一个空文件

    Args:
        path (_type_): _description_
        file_names (_type_): _description_
    """
    for name in filenames:
        with open(os.path.join(path_, name), "w"):
            pass


def test_remove_no_empty_folder() -> None:
    """
    删除一个非空目录

    如果目录下仅包含空目录, 则可以通过 os.removedirs 函数删除顶层目录
    但如果有任意子目录包含文件, 则都无法删除上层目录

    可以通过 shutil.rmtree 函数删除目录以及其下所有子目录和文件
    """
    sub_path = "b/c"

    full_path = os.path.join(PATH_1, sub_path)
    # 创建路径
    os.makedirs(full_path, mode=0o777, exist_ok=True)

    # 产生一系列文件名
    filenames = ["file_" + str(x) for x in range(1, 10)]
    # 在指定路径下创建一系列文件
    touch(full_path, filenames)

    # 确保文件创建成果
    assert set(os.listdir(full_path)) == set(filenames)

    # 由于路径下包含文件, 此时无法删除指定路径
    with raises(OSError):
        os.removedirs(PATH_1)

    # 删除路径连同其中的文件
    shutil.rmtree(PATH_1, ignore_errors=True)
    assert os.path.exists(PATH_1) is False


def test_rename_file_or_dir() -> None:
    """
    对文件 (或路径进行重命名)

    所谓重命名, 即将一个文件名称改为另一个文件名称, 或将一个路径名称改为另一个路径名称
    在此过程中, 文件或路径的内容和属性不变
    """
    def make_file_in_dir(dir=PATH_1, filename: str = None) -> str:
        """
        在指定路径下创建一个空文件

        Args:
            dir (str, optional): 文件路径. Defaults to PATH_1.
            filename (str, optional): 文件名. Defaults to None.

        Returns:
            str: 完整的文件路径名称
        """
        # 创建目标路径
        os.mkdir(dir)
        # 是否进一步创建文件
        if not filename:
            return dir

        # 创建一个空文件
        touch(dir, [filename])
        return os.path.join(dir, filename)

    # 测试对路径进行更名

    # 创建源文件, 获取源文件文件名
    src = make_file_in_dir(filename="src.txt")
    # 生产目标文件文件名
    dest = os.path.join(PATH_2, "src.txt")

    # 源文件存在
    assert os.path.exists(src) is True
    # 目标文件未产生
    assert os.path.exists(dest) is False

    # 对路径进行更名
    os.rename(PATH_1, PATH_2)

    # 源文件已不存在
    assert os.path.exists(src) is False
    # 目标文件已产生
    assert os.path.exists(dest) is True

    shutil.rmtree(PATH_2, ignore_errors=True)

    # 测试对文件进行更名

    # 创建源文件, 获取源文件文件名
    src = make_file_in_dir(filename="src.txt")
    dest = os.path.join(PATH_2, "dest.txt")
    # 源文件存在
    assert os.path.exists(src) is True
    # 目标文件未产生
    assert os.path.exists(dest) is False

    os.mkdir(PATH_2)
    os.rename(src, dest)

    # 源文件已不存在
    assert os.path.exists(src) is False
    # 目标文件已产生
    assert os.path.exists(dest) is True

    shutil.rmtree(PATH_2, ignore_errors=True)
