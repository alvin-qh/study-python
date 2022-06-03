import json
import os
from math import inf, nan
from typing import Any, Dict, Optional

from pytest import raises

# 字典对象转为 JSON 字符串


def test_dict_to_json() -> None:
    """
    将字典对象序列化为 json 字符串
    """
    data = {
        "name": "Alvin",
        "age": 40,
        "skill": [
            "Programming",
            "Teaching"
        ]
    }

    # 将字典对象转为 json 字符串
    s = json.dumps(data)

    assert s == (
        '{"name": "Alvin", "age": 40, '
        '"skill": ["Programming", "Teaching"]}'
    )


def test_dict_to_json_with_intent() -> None:
    """
    将字典对象序列化为 json 字符串, 对输出的 json 进行格式化

    通过 `indent=4` 参数设置 json 项的缩进
    """
    data = {
        "name": "Alvin",
        "age": 40,
        "skill": [
            "Programming",
            "Teaching"
        ]
    }

    # 将字典对象转为 json 字符串
    # indent=4 表示设置 json 格式缩进值为 4 个空白字符
    s = json.dumps(data, indent=4)

    # 输出格式化后的 json
    assert s == """{
    "name": "Alvin",
    "age": 40,
    "skill": [
        "Programming",
        "Teaching"
    ]
}"""


def test_dict_to_json_with_key_sorted() -> None:
    """
    对输出 json 的字段名进行排序

    按照字典序, 对输出的 json 字符串的字段进行排序, 确保不同系统输出的 json 字段顺序一致
    """
    data = {
        "name": "Alvin",
        "age": 40,
        "skill": [
            "Programming",
            "Teaching"
        ]
    }

    # sort_keys=True 表示需要对输出的 json 字段进行排序 (字典序)
    s = json.dumps(data, sort_keys=True, indent=4)

    # 输出格式化后的 json
    assert s == """{
    "age": 40,
    "name": "Alvin",
    "skill": [
        "Programming",
        "Teaching"
    ]
}"""


def test_nan_in_json() -> None:
    """
    `math` 包下的 `nan` 对象表示 Python 的 NaN, 表示 Not a Number

    在 json 中表示为 `NaN`
    """
    # 包含 NaN 的 json 字符串
    data = {
        "name": "Alvin",
        "age": nan,  # 数字类型以 NaN 表示, 即 float("nan")
        "skill": [
            "Programming",
            "Teaching"
        ]
    }

    # 允许 json 中包含 NaN
    s = json.dumps(data, indent=4)

    # 输出格式化后的 json, 包含 NaN
    assert s == """{
    "name": "Alvin",
    "age": NaN,
    "skill": [
        "Programming",
        "Teaching"
    ]
}"""

    # 可以禁止 json 中包含 NaN, 通过 allow_nan=False 禁止 json 中包含 NaN
    with raises(ValueError):  # 如果字典中包含 nan, 则抛出异常
        json.dumps(data, indent=4, allow_nan=False)


def test_inf_in_json() -> None:
    """
    `math` 包下的 `inf` 对象表示无穷大, 可以为 `inf` 和 `-inf`

    在 json 中表示为 `Infinity`
    """
    data = {
        "name": "Alvin",
        "age": inf,  # 无穷大表示为 inf, 即 float("inf")
        "skill": [
            "Programming",
            "Teaching"
        ]
    }

    s = json.dumps(data, indent=4)

    # 输出的 json 字符串包含 Infinity 表示无穷大
    assert s == """{
    "name": "Alvin",
    "age": Infinity,
    "skill": [
        "Programming",
        "Teaching"
    ]
}"""


# JSON 字符串转为字典对象

def test_json_to_dict() -> None:
    """
    json 字符串转为字典对象
    """
    s = """{
        "age": 40,
        "name": "Alvin",
        "skill": ["Programming", "Teaching"]
    }"""

    # 将字符串转为字典对象 (反序列化)
    data = json.loads(s)

    # 确认反序列化后的字典对象
    assert data == {
        "name": "Alvin",
        "age": 40,
        "skill": ["Programming", "Teaching"],
    }


# 和 IO 对象结合使用

# 存储结果的文件
FILE_NAME = "data.json"


def test_json_with_file_describer() -> None:
    """
    测试通过 IO 对象进行 json 序列化和反序列化

    即将字典对象序列化为字符串后写入 IO 对象, 或者从 IO 对象中读取 json 字符串并反序列化为字典对象
    """
    data = {
        "name": "Alvin",
        "age": 40,
        "skill": ["Programming", "Teaching"]
    }

    try:
        # 打开文件用于字符串写入 (必须以 "w" 文本方式打开)
        with open(FILE_NAME, "w") as fp:
            # 将字典对象写入文件
            json.dump(data, fp, indent=4)

        # 打开文件用于字符串读取 (必须以 "r" 文本方式打开)
        with open(FILE_NAME, "r") as fp:
            # 验证文件内容正确
            assert fp.read() == """{
    "name": "Alvin",
    "age": 40,
    "skill": [
        "Programming",
        "Teaching"
    ]
}"""
            # 将文件指针移动到开始 (重新读取文件)
            fp.seek(os.SEEK_SET)

            # 从文件中读取内容并反序列化为字典对象
            obj = json.load(fp)

        # 确认序列化前和反序列化后的对象相同
        assert obj == data
    finally:
        os.remove(FILE_NAME)


# 非字典对象和 json 字符串相互转换


class A:
    """
    用于测试自定义 json 序列化和反序列化的类型
    """

    def __init__(self, name: str, age: int) -> None:
        """
        初始化, 为对象设置属性值

        Args:
            name (str): 属性值
            age (int): 属性值
        """
        self.name = name
        self.age = age

    def __eq__(self, other: Any) -> bool:
        """
        判断两个对象类型是否相同

        Args:
            other (Any): 待比较对象

        Returns:
            bool: 待比较对象和当前对象是否相同
        """
        if not isinstance(other, A):
            return False

        return (
            other.name == self.name
            and other.age == self.age
        )


class ObjectEncoder(json.JSONEncoder):
    """
    编码器类型

    用于将指定类型的对象编码为 json 字符串
    """

    def default(self, obj: Any) -> Optional[Dict[str, Any]]:
        """
        将 `obj` 对象转为字典对象

        Args:
            obj (Any): 任意对象

        Returns:
            Optional[Dict[str, Any]]: 用于将对象转为 json 字符串的字典对象
        """
        if isinstance(obj, dict):
            # 字典类型对象, 返回对象本身
            return obj

        if isinstance(obj, A):
            # 指定类型对象, 返回该对象对应的字典对象
            return {
                "__custom__": True,
                "name": obj.name,
                "age": obj.age,
            }

        # 未指定类型对象, 返回对象对应的字典对象
        return obj.__dict__


def test_custom_json_encode() -> None:
    """
    测试 json 反序列化为自定义类型

    通过 `cls` 参数可以指定一个对象编码器类型, 用于将指定类型的对象转为 json
    """
    # 自定义类型对象
    src = A("Alvin", 40)
    # 指定序列化 encoder 类型
    s = json.dumps(src, cls=ObjectEncoder, indent=4)

    # 确保返回的 json 字符串正确
    assert s == """{
    "__custom__": true,
    "name": "Alvin",
    "age": 40
}"""


def _object_hook(data: Dict[str, Any]) -> Any:
    """
    将符合条件的字典对象转为对应类型的对象

    Args:
        data (Dict[str, Any]): 字典类型对象

    Returns:
        Any: 相关的自定义类型对象
    """
    # 判断字典对象中是否包含 __custom__ 字段
    if "__custom__" in data:
        # 返回转换结果为 A 类型对象
        return A(data["name"], data["age"])

    # 其它情况, 返回转换结果为字典类型对象
    return data


def test_custom_json_decoder() -> None:
    """
    测试将 json 字符串反序列化为自定义类型对象

    通过 `object_hook` 参数, 可以在转换时进行拦截处理, 将字典对象转为指定类型对象
    """
    # 待反序列化的 json 字符串
    s = """
    {
        "__custom__": true,
        "name": "Alvin",
        "age": 40
    }
    """

    # 指定 object_hook 参数
    dst = json.loads(s, object_hook=_object_hook)
    assert dst == A("Alvin", 40)
