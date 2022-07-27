# 使用 Matplot 绘制 3D 坐标

注意, 要让 `matplotlib` 库的 3D 绘图正常工作, 需要在编译 Python 时设置好 `Tcl/Tk` 的环境, 编译的 Python 才能支持 `python3-tk` 执行, 否则会引发类似如下错误:

```python
>>> import tkinter
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/lib/python3.8/tkinter/__init__.py", line 36, in <module>
    import _tkinter # If this fails your Python may not be configured for Tk
ModuleNotFoundError: No module named '_tkinter'
>>>
```

具体的方法为:

1. 安装 `Tcl/Tk` 开发库: 命令行 `sudo apt install tk-dev`
2. 安装对 Python 的支持: 命令行 `sudo apt install python3-tk`
3. 编译 Python, 这里以 `PyEnv` 工具为例: 命令行 `pyenv install 3.10.3`
4. 测试是否可以启用 `tkinter` 包: 命令行 `python -c "import tkinter"`
