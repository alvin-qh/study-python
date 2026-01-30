from typing import Any

# 定义 automate 参数类型
AutomateArgs = dict[str, Any] | list[Any] | set[Any] | tuple[Any, ...]


class Automate(dict[str, Any]):
    """属性自动组装类型

    该类可根据类中定义的 `__slots__` 字段自动装配对象属性值

    该类从 `dict` 类型继承, 底层存储为 Key/Value
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """初始化对象"""
        # 对位置参数进行处理
        for n, args in enumerate(args):
            # 将参数解析后和, 按照 __slots__ 对应位置参数名为 Key 进行存储
            self[self.__slots__[n]] = self._parse_args(args)

        # 对字典参数进行处理
        for key, args in kwargs.items():
            # 将参数解析后, 按照参数名为 Key 进行存储
            self[key] = self._parse_args(args)

    @staticmethod
    def _parse_args(args: AutomateArgs) -> "Automate" | AutomateArgs:
        """解析 `AutomateArgs` 类型参数

        - 对于参数类型为 `dict` 类型, 返回 `Automate` 类型对象
        - 对于参数类型为 `dict`, `set` 和 `tuple` 类型, 返回 `list[Automate]` 类型对象
        - 对于其它参数类型, 返回参数本身

        Returns:
            `"Automate" | AutomateArgs`: 返回解析后的参数
        """
        if isinstance(args, dict):
            # 将参数解析为 Automate 类型对象
            return Automate(**args)

        if isinstance(args, (list, set, tuple)):
            # 将参数解析为 Automate 列表类型对象
            return [Automate(**arg) if isinstance(arg, dict) else arg for arg in args]

        return args

    def __getattr__(self, name: str) -> Any:
        """根据属性名获取属性值

        Args:
            `name` (`str`): 属性名

        Returns:
            `Any`: 属性值
        """
        return self.get(name)

    def __setattr__(self, name: str, value: Any) -> None:
        """设置属性值

        Args:
            `name` (`str`): 属性名
            `value` (`Any`): 属性值
        """
        self[name] = value
