import csv
import os

FILE_NAME = "demo.csv"


def test_create_csv_file() -> None:
    """测试创建一个 csv 文件"""

    # 表头字段
    cols = ["Id", "Name", "Position"]

    # 4 行数据集合
    rows = [
        [1, "Alvin", "DEV"],
        [2, "Author", "BA"],
        [3, "Emma", "QA"],
        [4, "Tom", "PM"],
    ]

    try:
        # 打开文件用于写入 csv
        with open(FILE_NAME, "w", newline="") as fp:
            # 创建一个 writer 对象用于写入 csv 文件
            w = csv.writer(fp)
            # 写入表头
            w.writerow(cols)
            # 写入行数据集合
            w.writerows(rows)

        # 读取 csv 文件验证写入成功
        with open(FILE_NAME, "r") as fp:
            # 读取内容为写入的 csv 格式内容
            assert (
                fp.read()
                == """Id,Name,Position
1,Alvin,DEV
2,Author,BA
3,Emma,QA
4,Tom,PM
"""
            )
    finally:
        os.remove(FILE_NAME)


def test_read_csv_file() -> None:
    """测试读取 csv 文件"""

    try:
        # 将 csv 内容写入文件 (字符串形式)
        with open(FILE_NAME, "w") as fp:
            fp.write(
                """Id,Name,Position
1,Alvin,DEV
2,Author,BA
3,Emma,QA
4,Tom,PM
"""
            )
        # 读取方式打开文件, 用于读取 csv 内容
        with open(FILE_NAME, "r") as fp:
            # 创建一个 reader 对象用于读取 csv 内容
            r = csv.reader(fp)

            # 读取第一行内容, 为表头信息
            cols = next(r)
            assert cols == ["Id", "Name", "Position"]

            # 读取其余内容
            rows = [line for line in r]
            # 确保读取和写入内容一致
            assert rows == [
                ["1", "Alvin", "DEV"],
                ["2", "Author", "BA"],
                ["3", "Emma", "QA"],
                ["4", "Tom", "PM"],
            ]
    finally:
        os.remove(FILE_NAME)


def test_write_csv_as_dict() -> None:
    """以字典形式的数据写入 csv

    字典数据比上例中的列表数据更加直观, 通过 `DictWriter` 对象, 指定表头字段后, 即可以以表头字段为 Key 的字典数据写入内容
    """
    # 表头集合
    cols = ["Id", "Name", "Position"]

    # 内容, 为字典对象集合
    rows = [
        {"Id": 1, "Name": "Alvin", "Position": "DEV"},
        {"Id": 2, "Name": "Author", "Position": "BA"},
        {"Id": 3, "Name": "Emma", "Position": "QA"},
        {"Id": 4, "Name": "Tom", "Position": "PM"},
    ]

    try:
        # 打开文件用于写入 csv 内容
        with open(FILE_NAME, "w+", newline="") as fp:
            # 创建一个字典 writer 用于写入字典内容
            # fieldnames 用于指定表头字段名, 也作为字典项目的 key
            w = csv.DictWriter(fp, fieldnames=cols)
            # 写入表头
            w.writeheader()

            # 写入行数据
            w.writerows(rows)

        # 读取 csv 文件验证写入成功
        with open(FILE_NAME, "r") as fp:
            # 读取内容为写入的 csv 格式内容
            assert (
                fp.read()
                == """Id,Name,Position
1,Alvin,DEV
2,Author,BA
3,Emma,QA
4,Tom,PM
"""
            )
    finally:
        os.remove(FILE_NAME)
