import io
import pickle
from typing import Any


class Person:
    """
    测试序列化的类
    """

    def __init__(self, id_: int, name: str, message: str) -> None:
        """
        初始化对象
        """
        self.id = id_
        self.name = name
        self.message = message

    def __eq__(self, other: Any) -> bool:
        """
        比较两个对象是否相同

        Args:
            other (Any): 要比较的对象

        Returns:
            bool: 当前对象和要比较的对象是否相同
        """
        # 判断当前对象和待比较对象类型是否相同
        if self.__class__ != other.__class__:
            return False

        # 判断两个对象字段值是否相同
        return (
            self.id == other.id
            and self.name == other.name
            and self.message == other.message
        )


def test_dump_load_function() -> None:
    """
    测试通过 `pickle` 包的 `dump` 函数可以将一个对象进行序列化并存储到 IO 对象中
    """
    # 字典对象序列化

    # 产生一个字典对象
    obj = {
        "id": 1,
        "name": "Alvin",
        "message": "Hello World",
    }

    # 测试字典序列化到文件
    with io.BytesIO() as fp:
        # 序列化字典对象
        pickle.dump(obj, fp)

        # 获取序列化后的数据
        data = fp.getvalue()
        assert len(data) > 0

    # 测试从文件中反序列化对象
    with io.BytesIO(data) as fp:
        # 反序列字典对象, 确保和源对象相同
        assert pickle.load(fp) == obj

    # 类对象序列化

    # 测试类对象序列化到文件
    with io.BytesIO() as fp:
        # 产生一个类对象
        psn = Person(1, "Alvin", "Hello World")

        # 序列化类对象
        pickle.dump(psn, fp)

        # 获取序列化后的数据
        data = fp.getvalue()
        assert len(data) > 0

    # 测试从文件中反序列化类对象
    with io.BytesIO(data) as fp:
        # 反序列类对象对象, 确保和源对象相同
        assert pickle.load(fp) == psn


def test_dumps_loads_function() -> None:
    """
    测试通过 `pickle` 包的 `dumps` 函数可以将一个对象进行序列化
    """
    # 字典对象序列化

    # 产生一个字典对象
    obj = {
        "id": 1,
        "name": "Alvin",
        "message": "Hello World",
    }

    # 序列化字典对象
    s = pickle.dumps(obj)
    assert len(s) > 0

    # 反序列字典对象, 确保和源对象相同
    assert pickle.loads(s) == obj

    # 类对象序列化

    # 产生一个类对象
    psn = Person(1, "Alvin", "Hello World")

    # 序列化类对象
    s = pickle.dumps(psn)
    assert len(s) > 0

    # 反序列类对象对象, 确保和源对象相同
    assert pickle.loads(s) == psn
