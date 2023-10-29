# Blinker

> [Document](https://pythonhosted.org/blinker/)

## Named Signals

```python
from blinker import signal

on_initialized = signal('initialized')  # define a named signal
```

## Subscribing to Signals

```python
def initialized_subscriber(*args, **kwargs):
    ...
    return ...

on_initialized.connect(initialized_subscriber)
```

Also can connection subscriber by decorate

```python
@on_initialized.connect
def initialized_subscriber(*args, **kwargs):
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
