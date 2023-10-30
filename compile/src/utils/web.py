import os
import time
from functools import wraps
from typing import Any, Callable, Dict, Optional
from urllib.parse import parse_qs

import xxhash

from flask import Flask, json, render_template, request


def templated(template: Optional[str] = None) -> Callable[..., Any]:
    def decorator(f: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(f)
        def decorated_function(*args: Any, **kwargs: Any) -> Any:
            if template:
                template_name = template
            elif request.endpoint:
                template_name = request.endpoint.replace(".", "/") + ".html"
            else:
                raise FileNotFoundError("no template")

            ctx, code = f(*args, **kwargs), 200
            if isinstance(ctx, tuple):
                ctx, code = ctx

            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx

            return render_template(template_name, **ctx), code

        return decorated_function

    return decorator


class Assets:
    def __init__(self, app: Flask) -> None:
        assert app.static_folder

        self._static_folder = app.static_folder
        self._static_url_path = app.static_url_path
        self._asset_file_cache = {}
        self._debug = app.debug

        assert app.static_folder
        manifest_file = os.path.join(app.static_folder, "manifest.json")
        if os.path.exists(manifest_file):
            with open(manifest_file, "r", encoding="utf8") as f:
                self._asset_file_cache = json.loads(f.read())

    def image(self, key: str, fixed: bool = False) -> str:
        return self._asset(f"images/{key}", fixed)

    def css(self, key: str, fixed: bool = False) -> str:
        return self._asset(f"css/{key}", fixed)

    def js(self, key: str, fixed: bool = False) -> str:
        return self._asset(f"js/{key}", fixed)

    def _calculate_asset_hash(self, asset_file: str) -> str:
        hash_ = ""
        file = os.path.join(self._static_folder, asset_file)
        if os.path.isfile(file):
            with open(file, "rb") as f:
                hash_ = xxhash.xxh64(f.read()).hexdigest()

        return hash_

    def _asset(self, filename: str, fixed: bool) -> str:
        if self._debug and not fixed:
            return f"{self._static_url_path}/{filename}?__v={time.time()}"

        if filename in self._asset_file_cache:
            filename = self._asset_file_cache[filename]
            return f"{self._static_url_path}/{filename}"

        hash_ = self._calculate_asset_hash(filename)
        uri = f"{filename}?__v={hash_}"
        self._asset_file_cache[filename] = uri

        return f"{self._static_url_path}/{uri}"


class HttpMethodOverrideMiddleware:
    allowed_methods = frozenset(
        ["GET", "HEAD", "POST", "DELETE", "PUT", "PATCH", "OPTIONS"]
    )

    body_less_methods = frozenset(["GET", "HEAD", "OPTIONS", "DELETE"])

    def __init__(self, wsgi_app: Callable[..., Any], name: str = "__method") -> None:
        self._app = wsgi_app
        self._name = name

    def __call__(self, environ: Dict[str, Any], start_response: Any) -> Any:
        if environ.get("REQUEST_METHOD", "") == "POST":
            qs = environ.get("QUERY_STRING", "")
            if self._name in qs:
                method = parse_qs(qs).get(self._name, ["GET"])[0]

                if method in self.allowed_methods:
                    environ["REQUEST_METHOD"] = method

                if method in self.body_less_methods:
                    environ["CONTENT_LENGTH"] = "0"

        return self._app(environ, start_response)
