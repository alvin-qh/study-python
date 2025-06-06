import io
import pickle

from basic.io_.model import PersonModel


def test_dump_load_function() -> None:
    """测试 `pickle` 包的 `dump` 函数

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
        psn = PersonModel(1, "Alvin", "Hello World")

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
    """测试 `pickle` 包的 `dumps` 函数

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
    psn = PersonModel(1, "Alvin", "Hello World")

    # 序列化类对象
    s = pickle.dumps(psn)
    assert len(s) > 0

    # 反序列类对象对象, 确保和源对象相同
    assert pickle.loads(s) == psn
