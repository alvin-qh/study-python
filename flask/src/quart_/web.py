from functools import wraps
from typing import Any, Callable, Optional, Tuple, Union

from quart import render_template, request
from utils import TemplateResolveError


async def return_or_render(
    template: Optional[str], result: Any
) -> Union[Any, Tuple[str, int]]:
    """根据路由函数的返回值, 返回模板 (异步渲染) 或其它响应结果

    Args:
        - `template` (`str`): 模板名称
        - `result` (`Any`): 路由函数结果

    Returns:
        `Union[Any, Tuple[str, int]]`: 请求结果或模板渲染结果
    """
    # 如果路由结果为 tuple 类型, 则取出 ctx 和 code 两个结果
    if isinstance(result, tuple):
        ctx, code = result
    else:
        # 如果路由结果只返回一个值, 则 code 默认为 200
        ctx, code = result, 200

    if ctx is None:
        ctx = {}
    elif not isinstance(ctx, dict):
        # 如果返回的 ctx 不为字典类型, 则不渲染模板, 返回此结果即可
        return ctx

    # 计算模板名称，如果未传递 template 参数，则用当前请求的路径作为模板文件路径名
    template_name = template
    if not template_name:
        # 根据请求的的 endpoint 计算模板名称
        if request.endpoint:
            template_name = f'{request.endpoint.replace(".", "/")}.html'
        else:
            raise TemplateResolveError("No template valid")

    # 执行异步模板渲染
    return await render_template(template_name, **ctx), code


def templated(template: Optional[str] = None) -> Callable[..., Any]:
    """模板文件装饰器

    该装饰器用于修饰控制器函数, 将控制器函数返回的结果传递到指定的 html 模板上并进行渲染

    Args:
        - `template` (`Optional[str]`): 模板名称, `None` 表示根据规则取默认模板

    Returns:
        `Callable[..., Any]`: 被装饰方法
    """

    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        """定义装饰器方法"""

        @wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            """定义包装函数 (异步执行)"""

            # 根据计算得到的模板名称渲染 html
            return await return_or_render(template, await fn(*args, **kwargs))

        return wrapper

    return decorator
