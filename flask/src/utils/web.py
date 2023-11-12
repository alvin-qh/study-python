import os
import time
from functools import wraps
from typing import Any, Callable, Dict, Optional

import xxhash
from flask import Flask, json, render_template, request
from urllib.parse import parse_qs


class TemplateResolveError(Exception):
    """HTML 模板无法解析异常"""


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
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """定义包装函数"""

            # 计算模板名称，如果未传递 template 参数，则用当前请求的路径作为模板文件路径名
            template_name = template
            if not template_name:
                if request.endpoint:
                    template_name = f'{request.endpoint.replace(".", "/")}.html'
                else:
                    raise TemplateResolveError("No template valid")

            # 调用 controller 函数
            ctx, code = fn(*args, **kwargs), 200  # 默认 http code 为 200
            # 如果函数返回了 http code，则替换默认的 code
            if isinstance(ctx, tuple):
                ctx, code = ctx

            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx

            # 根据计算得到的模板名称渲染 html
            return render_template(template_name, **ctx), code

        return wrapper

    return decorator


class AssetError(Exception):
    """HTML 模板无法解析异常"""


class Assets:
    """访问静态资源的工具类"""

    def __init__(self, app: Flask) -> None:
        # 获取静态文件路径
        self._static_folder = app.static_folder

        # 获取静态文件 URL
        self._static_url_path = app.static_url_path

        # 静态文件文件缓存
        self._asset_file_cache = {}

        # 是否调试模式
        self._debug = app.debug

        # 获取静态资源描述文件路径
        if not app.static_folder:
            raise AssetError("`app.static_folder` not set")

        manifest_file = os.path.join(app.static_folder, "manifest.json")

        if os.path.exists(manifest_file):
            with open(manifest_file, "r") as fp:
                # 读取描述文件内容
                self._asset_file_cache = json.loads(fp.read())

    def image(self, key: str, fixed: bool = False) -> str:
        """读取图片静态资源

        Args:
            - `key` (`str`): 资源 key
            - `fixed` (`bool`, optional): 资源是否不会发生变化. Defaults to `False`.

        Returns:
            `str`: 图片静态资源路径
        """
        return self._asset(f"images/{key}", fixed)

    def css(self, key: str, fixed: bool = False) -> str:
        """读取 CSS 静态资源

        Args:
            - `key` (`str`): 资源 key
            - `fixed` (`bool`, optional): 资源是否不会发生变化. Defaults to `False`.

        Returns:
            `str`: css 静态资源路径
        """
        return self._asset(f"css/{key}", fixed)

    def script(self, key: str, fixed: bool = False) -> str:
        """读取脚本静态资源

        Args:
            - `key` (`str`): 资源 key
            - `fixed` (`bool`, optional): 资源是否不会发生变化. Defaults to `False`.

        Returns:
            `str`: 脚本静态资源路径
        """
        return self._asset(f"script/{key}", fixed)

    def _asset(self, filename: str, fixed: bool) -> str:
        """获取静态资源的 URL 路径

        Args:
            - `filename` (`str`): 静态文件名称
            - `fixed` (`bool`): 资源是否不会发生变化

        Returns:
            `str`: 静态资源路径
        """

        # 对于调试模式或非固定静态资源，直接在 URL 后加随机数，防止资源被缓存
        if self._debug and not fixed:
            return f"{self._static_url_path}/{filename}?__v={time.time()}"

        # 尝试从缓存中获取（具备静态资源描述文件的情况）
        if filename in self._asset_file_cache:
            return f"{self._static_url_path}/{self._asset_file_cache[filename]}"

        hash_ = self._calculate_asset_hash(filename)
        uri = f"{filename}?__v={hash_}"
        self._asset_file_cache[filename] = uri

        return f"{self._static_url_path}/{uri}"

    def _calculate_asset_hash(self, asset_file: str) -> str:
        """
        计算静态资源的 hash 后缀（防止被缓存）

        Args:
            - `asset_file` (`str`): 静态资源文件名

        Returns:
            `str`: 静态资源的 hash 值
        """

        if not self._static_folder:
            raise AssetError("`app.static_folder` not set")

        # 缓存中获取失败后，开始计算 hash 值
        file = os.path.join(self._static_folder, asset_file)
        if not os.path.isfile(file):
            raise AssetError(f"'{file}' is not a asset file")

        with open(file, "rb") as fp:
            return xxhash.xxh64(fp.read()).hexdigest()


class HttpMethodOverrideMiddleware:
    """用于修改请求 Http 方法的中间件类

    该类的主要作用是将 <form> 表单的请求方式进行处理，<form> 表单只具备 GET, POST 两种请求方式
    对于 POST 表单提交，可以根据其携带的参数（例如："__method"），转化为 PUT, DELETE 等请求方式
    """

    # 定义请求中允许的 http 方法
    allowed_methods = frozenset(
        [
            "GET",
            "HEAD",
            "POST",
            "DELETE",
            "PUT",
            "PATCH",
            "OPTIONS",
        ]
    )

    # 定义 body 为空的 http 方法
    body_less_methods = frozenset(
        [
            "GET",
            "HEAD",
            "OPTIONS",
            "DELETE",
        ]
    )

    def __init__(self, wsgi_app: Callable[..., Any], name: str = "__method") -> None:
        """
        初始化当前中间件对象

        Args:
            wsgi_app (Callable): Flask 中间件调用链
            name (str, optional): 用于表示请求方法的参数名称. Defaults to "__method".
        """
        self._app = wsgi_app
        self._name = name

    def __call__(self, environ: Dict[str, Any], start_response: Any) -> Any:
        """调用中间件

        Args:
            - `environ` (`Dict[str, Any]`): 保存请求相关参数的字典对象
        """

        # 判断是否为 POST 请求，只有 POST 请求可能需要被转换
        if environ.get("REQUEST_METHOD", "") == "POST":
            # 获取请求参数字符串，并判断预设的参数名是否包含在内
            qs = environ.get("QUERY_STRING", "")
            if qs:
                # 从请求参数中获取预设的参数
                method = parse_qs(qs).get(self._name, ["GET"])[0]
                if method:
                    # 将当前请求的请求方式替换
                    if method in self.allowed_methods:
                        environ["REQUEST_METHOD"] = method

                    # 对于 bodyless 类型的请求，处理一下 content_length 参数
                    if method in self.body_less_methods:
                        environ["CONTENT_LENGTH"] = "0"

        # 调用下一个中间件对象
        return self._app(environ, start_response)
