# 从子模块导入所需类, 函数或值
# 其它模块既可以从当前包导入所需的内容
from .func import Class, function, value

# 指定当前模块默认开放的内容, 当使用 `from ... import *` 时, 只会导入 `__all__` 中定义的部分
__all__ = [
    "Class",
    "function",
    "value",
    "version",
]


# 定义全局变量值
version = "1.0"
