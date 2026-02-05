from functools import wraps
from typing import Any, Callable, Self, Type


class Delegate:
    """定义代理类型

    代理类型用于代理另一个对象, 让自身的对象具备被代理对象的所有属性和方法, 令代理对象和被代理对象看起来一模一样

    代理对象可以被当作被代理对象来使用, 并且可以在访问被代理对象的属性和方法时, 执行额外的代码, 起到不修改被代理对象类型,
    可以改变被代理对象的属性和方法执行逻辑
    """

    def __init__(self, inst: Any) -> None:
        """初始化代理对象

        Args:
            `inst` (`Any`): 被代理的对象实例
        """
        self._inst = inst

    def __getattribute__(self, name: str) -> Any:
        """获取对象的属性和方法

        Args:
            `name` (`str`): 属性名

        Returns:
            `Any`: 属性值
        """
        # 获取名为 _inst 属性
        # 通过 object 的 __getattribute__ 方法获取 _inst 属性,
        # 防止当前的 __getattribute__ 方法被重复无限调用
        inst = object.__getattribute__(self, "_inst")

        # 判断所需属性名是否在被代理对象中
        if hasattr(inst, name):
            # 从被代理对象中获取属性值
            attr = getattr(inst, name)

            # 判断返回的属性是否为可调用对象
            if callable(attr):
                # 将调用进行包装后, 返回代理函数
                return self._wrapper(attr)

            # 返回属性值
            return attr

        # 如果属性未被定义, 则返回代理类型本身的属性值
        return object.__getattribute__(self, name)

    def _wrapper(self, fn: Callable[..., Any]) -> Callable[..., Any]:
        """对指定的函数 (方法) 进行代理, 返回代理函数 (方法) 对象

        Args:
            `fn` (`Callable`): 被代理函数 (方法)

        Returns:
            `Callable`: 代理函数 (方法)
        """

        @wraps(fn)
        def func(*args: Any, **kwargs: Any) -> str:
            """代理函数 (方法)

            Returns:
                `str`: 将被代理函数 (方法) 返回值格式化后的结果
            """
            return f"Result is: {fn(*args, **kwargs)}"

        return func

    @property
    def __class__(self) -> Type[Self]:
        """重写代理类型的获取类的方法, 返回被代理对象的类型

        Returns:
            `Any`: 被代理对象的类型
        """
        return type(self._inst)

    @__class__.setter
    def __class__(self, __type: type[object]) -> None:  # noqa
        pass

    def __ins

    @property
    def instance(self) -> Any:
        """获取被代理对象实例

        Returns:
            `Any`: 被代理对象实例
        """
        return self._inst
