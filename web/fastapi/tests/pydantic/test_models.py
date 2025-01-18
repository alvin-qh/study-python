import json
from pydantic_.models import Org


def test_org_to_json() -> None:
    """测试将 `Org` 类型对象转为字典和 JSON 字符串

    字典的 `key` 为 `Org` 类的字段, 值即为字段值
    """

    org = Org(
        id=1001,
        name="Alvin",
    )

    # 将 `Org` 对象转为字典对象
    dump = org.model_dump()
    result = {k: v for k, v in dump.items() if k in ["id", "name"]}

    assert result == {
        "id": 1001,
        "name": "Alvin",
    }

    # 将 `Org` 对象转为 JSON 字符串后进一步转为字典对象
    dump = json.loads(org.model_dump_json())
    result = {k: v for k, v in dump.items() if k in ["id", "name"]}

    assert result == {"id": 1001, "name": "Alvin"}


def test_org_from_json() -> None:
    """测试从字典对象或者 JSON 字符串产生 `Org` 类型对象"""

    # 利用 `Org` 类型构造器, 通过字典对象产生 `Org` 对象
    org = Org(**{"id": 1001, "name": "Alvin"})
    assert org.id == 1001
    assert org.name == "Alvin"

    # 利用 `Org` 类型的 `model_validate` 方法, 通过字典对象产生 `Org` 对象
    org = Org.model_validate({"id": 1001, "name": "Alvin"})
    assert org.id == 1001
    assert org.name == "Alvin"

    # 利用 `Org` 类型的 `model_validate_json` 方法, 通过 JSON 字符串产生 `Org` 对象
    org = Org.model_validate_json('{"id":1001,"name":"Alvin"}')
    assert org.id == 1001
    assert org.name == "Alvin"
