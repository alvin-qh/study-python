# Blinker

> [Document](https://pythonhosted.org/blinker/)

## 命名信号

通过 `signal` 函数创建一个命名信号对象, 并通过一个全局变量进行引用

```python
from blinker import signal

on_initialized = signal('initialized')  # define a named signal
```

## 订阅信号

定义一个信号处理函数 (handler), 并通过信号对象的 `.connect` 方法将信号和处理函数进行关联

```python
def initialized_subscriber(*args, **kwargs):
    """定义信号处理函数"""
    ...
    return ...

# 将信号和信号处理函数进行关联
on_initialized.connect(initialized_subscriber)
```

可以通过装饰器方式进行关联

```python
@on_initialized.connect
def initialized_subscriber(*args, **kwargs):
    """定义信号处理函数, 并通过装饰器和"""
    ...
    return ...
```

## Emitting Signals

```python
on_initialized.send(...)
```

## Anonymous Signals

```python
from blinker import Signal

on_ready = Signal()
on_complete = Signal()
```
