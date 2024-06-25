# 美化错误输出

## 1. 概述

参考: <https://github.com/onelivesleft/PrettyErrors/>

通过 `pretty_errors` 库可以对 Python 中的异常输出进行美化, 使得异常报告更为清晰易读

## 2. 安装

可以直接通过 pip 工具安装

```bash
pip install pretty_errors
```

活着

```bash
python -m pip install pretty_errors
```

但使用工程化的包管理器安装更好, 以 PDM 包管理器为例, 可以将 `pretty_errors` 安装在 `dev` 或指定分组下, 由此在生产环境可以不安装 `pretty_errors`, 以保证不损失性能

安装到 `debug` 分组

```bash
pdm add pretty_errors -G debug
```

或者安装为开发环境依赖

```bash
pdm add pretty_errors --dev
```

所以, 当执行 `pdm install --prod` 命令时, 不会安装 `pretty_errors` 依赖包

## 3. 使用

`pretty_errors` 的使用非常简单, 只需要将其导入到当前项目即可, 即:

```python
import pretty_errors
```

之后所有输出异常信息的位置, 都回通过 `pretty_errors` 进行美化

如果需要对 `pretty_errors` 进行额外配置, 可以通过其 `configure` 函数, 即

```python
import pretty_errors

pretty_errors.configure(
    separator_character="*",
    filename_display=pretty_errors.FILENAME_EXTENDED,
    line_number_first=True,
    display_link=True,
    lines_before=5,
    lines_after=2,
    line_color=pretty_errors.RED
    + "> "
    + pretty_errors.default_config.line_color,
    code_color="  " + pretty_errors.default_config.line_color,
    truncate_code=True,
    display_locals=True,
)
```

可以将 `pretty_errors` 封装到一个模块中, 并通过一个初始化函数统一进行初始化, 而且可以针对 `pretty_errors` 依赖不存在的情况进行异常处理, 参考 [src/pretty/\_\_init\_\_.py](./src/pretty/__init\__.py) 文件
