import io
import json
from typing import Any, Callable


def tag(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    定义一个函数型装饰器

    装饰器函数的参数是被装饰函数, 返回被装饰后的代理函数

    Args:
        func (Callable[..., Any]): 被装饰函数

    Returns:
        Callable[..., Any]: 装饰后的代理函数
    """
    def wrapper(*args: Any, **kwargs: Any) -> str:
        """
        代理函数

        在代理函数中调用被装饰的函数

        Returns:
            str: 返回包含被代理函数返回值的 json 字符串
        """
        # 将被装饰函数的返回值放在一个 json 中
        result = {
            "wrapped": True,
            "result": func()
        }
        # 返回 json 字符串
        return json.dumps(result)

    # 返回代理函数, 取代被装饰函数
    return wrapper


def html_tag(tag_name: str, **kwargs: Any) -> Callable[..., Any]:
    """
    通过闭包创建装饰器函数

    通过闭包返回一个装饰器函数, 可以为装饰器函数引入参数

    装饰器函数将被装饰函数返回值包装为指定的 HTML 标签并返回

    Args:
        tag_name (str): HTML 标签名称, 该参数可以传递到内部的闭包函数
        kwargs(Dict[str, Any]): HTML 标签属性

    Returns:
        Callable: 装饰器函数
    """
    attribute = kwargs

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        定义装饰器函数, 为一个内部函数, 可以通过闭包方式获取外部定义的参数

        Args:
            func (Callable): 被装饰的函数

        Returns:
            Callable: 被装饰函数的代理函数
        """

        def wrapper(*args: Any, **kwargs: Any) -> str:
            """
            被装饰函数的代理函数

            Returns:
                str: 包装后的 HTML 标签
            """
            sio = io.StringIO()
            sio.write("<")
            sio.write(tag_name)

            for key in sorted(attribute.keys()):
                sio.write(" ")
                sio.write("class" if key == "clazz" else key)
                value = str(attribute[key])

                if value.find("\"") < 0:
                    sio.write("=\"")
                    sio.write(value)
                    sio.write("\"")
                else:
                    sio.write("=\'")
                    sio.write(value)
                    sio.write("\'")

            nested = func()
            if len(nested) == 0:
                sio.write("/>")
            else:
                sio.write(">")
                sio.write(nested)
                sio.write("</")
                sio.write(tag_name)
                sio.write(">")

            sio.seek(0)
            return sio.read()

        return wrapper

    return decorator


class HtmlTag:
    """
    将 Callable 类型对象作为函数装饰器

    装饰器类将被装饰函数返回值包装为指定的 HTML 标签并返回
    """

    def __init__(self, tag_name: str, **kwargs: Any) -> None:
        """
        构造器, 传递装饰器所需的参数

        Args:
            tag_name (str): HTML 标签名称
            kwargs(Dict[str, Any]): HTML 标签属性
        """
        self._kwargs = kwargs
        self._tag_name = tag_name

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """
        仿函数调用方法, 对被装饰函数进行包装, 返回被装饰函数的代理函数

        Args:
            func (Callable): 被装饰函数

        Returns:
            Callable: 被装饰函数的代理函数
        """

        def wrapper(*args: Any, **kwargs: Any) -> str:
            """
            被装饰函数的代理函数

            Returns:
                str: 包装后的 HTML 标签
            """
            sio = io.StringIO()
            sio.write("<")
            sio.write(self._tag_name)

            for key in sorted(self._kwargs):
                sio.write(" ")
                sio.write("class" if key == "clazz" else key)
                value = str(self._kwargs[key])

                if value.find("\"") < 0:
                    sio.write("=\"")
                    sio.write(value)
                    sio.write("\"")
                else:
                    sio.write("=\'")
                    sio.write(value)
                    sio.write("\'")

            nested = func()
            if len(nested) == 0:
                sio.write("/>")
            else:
                sio.write(">")
                sio.write(nested)
                sio.write("</")
                sio.write(self._tag_name)
                sio.write(">")

            sio.seek(0)
            return sio.read()

        return wrapper
