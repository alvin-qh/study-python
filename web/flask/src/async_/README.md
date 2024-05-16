# Flask[async]

Flask 可支持 Python3 的 `async` 协程, 可以在路由, 错误处理, 请求前后的处理函数都可以为协程函数

## 1. 安装依赖

异步 Flask 的依赖由 `Flask` 变更为 `Flask[async]`, 即通过如下命令安装

```bash
pip install 'Flask[async]'
```

或

```bash
pdm add 'Flask[async]'
```

## 2. 异步请求

注意, Flask 异步并不表示一个 worker 可以同时处理多个请求, 每个请求仍只能绑定在一个 worker 之上, 只是因为使用了 `async` 函数, 所以在每次请求中, 利用协程异步处理 IO 或异步访问数据库成为可能

## 3. 使用 Quart

Quart 是 Flask 的一个异步优先实现, 其基于 ASGI 标准 (而非 WSGI), 使其比标准 Flask 具备更好的异步性能, 具体的范例参考 `src/quart_` 范例
