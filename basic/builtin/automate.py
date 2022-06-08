from ast import Dict
from typing import Any, List, Set, Tuple

AnyArgs = Dict | List | Set | Tuple


class Automate(dict):
    """
    属性自动组装类型

    该类型从 Dict 类型继承, 底层存储为 Key/Value
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        初始化对象
        """
        # 对位置参数进行处理
        for n, val in enumerate(args):
            # 将参数解析后和, 按照 __slots__ 对应位置参数名为 Key 进行存储
            self[self.__slots__[n]] = self._parse_val(val)

        # 对字典参数进行处理
        for key, val in kwargs.items():
            # 将参数解析后, 按照参数名为 Key 进行存储
            self[key] = self._parse_val(val)

    @staticmethod
    def _parse_val(val: AnyArgs) -> "Automate" | AnyArgs:
        """
        解析

        Returns:
            _type_: _description_
        """
        if isinstance(val, dict):
            return Automate(**val)

        if isinstance(val, (list, set, tuple)):
            return [Automate(**v) if isinstance(v, dict) else v for v in val]

        return val

    def __getattr__(self, name: str) -> Any:
        return self.get(name)

    def __setattr__(self, name: str, value: Any):
        self[name] = value
