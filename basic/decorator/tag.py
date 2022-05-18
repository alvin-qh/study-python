import io
import json
from typing import Callable


def tag(func: Callable) -> Callable:
    """
    定义一个装饰器函数

    装饰器函数的参数是被装饰函数, 返回被装饰后的代理函数

    Args:
        func (Callable): 被装饰函数

    Returns:
        Callable: 装饰后的代理函数
    """
    def wrapper(*args, **kwargs) -> str:
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


def html_tag(tag_name: str, **kwargs) -> Callable:
    attribute = kwargs

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> str:
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
    def __init__(self, tag_name: str, **kwargs) -> None:
        self._kwargs = kwargs
        self._tag_name = tag_name

    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> str:
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
