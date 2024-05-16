# Flask 上下文钩子

- [Flask 上下文钩子](#flask-上下文钩子)
  - [1. 通过装饰器使用](#1-通过装饰器使用)
    - [1.1. 对于 `Flask` 对象](#11-对于-flask-对象)
    - [1.2. 对于 `Blueprint` 对象](#12-对于-blueprint-对象)
  - [2. 不使用装饰器](#2-不使用装饰器)

## 1. 通过装饰器使用

### 1.1. 对于 `Flask` 对象

```python
from flask import Flask

app = Flask(...)

# 对首次请求进行回调处理
@app.before_first_request
def before_first_request():
    ...

# 在每次请求之前进行回调处理
@app.before_request
def before_request():
    ...

# 在每次响应之后回调处理
@app.after_request
def after_request(response):
    ...

# 在每次会话之后进行回调处理
@app.teardown_request
def teardown_request(exception):
    ...
```

### 1.2. 对于 `Blueprint` 对象

```python
from flask import Blueprint

bp = Blueprint(...)

# 和 @app.before_first_request 对应
@bp.before_app_first_request()
def before_app_first_request():
    ...

# 和 @app.before_request 对应
@bp.before_app_request()
def before_app_request():
    ...

# 和 @app.before_request 对应, 但只在当前路由下起作用
@bp.before_request
def before_request():
    ...

# 和 @app.after_request 对应, 但只在当前路由下起作用
@bp.after_request
def after_request(response):
    ...

# 和 @app.teardown_request 对应, 但只在当前路由下起作用
@bp.teardown_request
def teardown_request(exception):
    ...
```

## 2. 不使用装饰器

```python
from flask import Flask

app = Flask(...)

def before_request():
    ...

app.before_request(_before_request)
```
