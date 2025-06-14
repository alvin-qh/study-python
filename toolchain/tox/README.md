# Tox

Tox 是一个 Python 上的测试管理框架, 可以按分类执行多组测试, 包括不同 Python 版本或不同依赖包版本, 也可以包括单元测试, 集成测试, 代码样式检查, 类型检查等

## 1. 安装

Tox 就是一个 Python 包, 所以可以通过各种方式安装, 包括通过 pip, uv, pdm, poetry 等

Pip

```bash
pip install tox
```

UV

```bash
uv add tox --dev
# 或
uv tool install tox
```

PDM

```bash
pdm add tox --dev
```

Poetry

```bash
poetry add tox --dev
```

## 2. 配置

当前路径下的如下文件均可以作为 tox 配置文件:

- `tox.ini`
- `setup.cfg` (也为 `ini` 格式)
- `pyproject.toml`
- `tox.toml`

更多配置相关内容参考 <https://tox.wiki/en/latest/config.html>

### 2.1 tox.toml

TOML 文件具有丰富的结构化格式和语法, 故作为 Tox 的配置文件的首选

#### 2.1.1. 顶层配置

在整个文件顶层, 可用于配置 Tox 的全局设置

```toml
requires = ["tox>=4.19"]
env_list = [
    "py313", # 可以写为 "3.13"
    "py312", # 可写写为 "3.12"
    "type",
    "lint",
]
```

其中:

- `requires`: 用于配置 Tox 的最低版本
- `env_list`: 用于配置 Tox 启用的环境名称列表, 每个环境都表示一个独立的虚拟环境, 且相互隔离
  - 名称为 `py312` 或 `3.12` 的环境, 表示需要特定的 Python 版本来执行的环境;
  - 其它名称的环境表示使用当前 Python 版本来执行的环境;
  - 这里只是配置要启用的环境名称, 具体环境的配置需要按后续步骤单独提供;

#### 2.1.2. 公共环境配置

公共环境配置用于所有环境, 相当于各环境的一个通用配置. 公共环境配置位于 `[env_run_base]` 段内

```toml
[env_run_base]
description = "..."
deps = [
    "pytest>=8.3",
]
commands = [
    ["pytest"],
]
allowlist_externals = ["pytest"]
```

其中:

- `deps`: 表示公共环境下依赖的包;
- `commands`: 表示公共环境下会执行的外部命令;
- `allowlist_externals`: 表示允许在公共环境下执行的外部命令;

上面范例中的配置表示在公共环境下配置了 `pytest` 依赖和命令, 所以无论执行任何环境, 都会先执行公共环境下的 `pytest` 命令

#### 2.1.3. 特殊 Python 版本环境配置

如果要为特殊 Python 版本设置环境, 可以配置为

```toml
[env.py313]
description = "..."
deps = ["..."]
commands = ["..."]

[env.py312]
description = "..."
deps = ["..."]
commands = ["..."]
```

上述配置对应顶层配置中 `env_list` 配置项的 `py312` 和 `py313` 项

如果使用类似 `3.12`, `3.13` 等格式定义的环境名称, 则配置环境时, 需要在配置段名称上额外增加引号, 如:

```toml
[env."3.12"]
description = "..."
deps = ["..."]
commands = ["..."]

[env."3.13"]
description = "..."
deps = ["..."]
commands = ["..."]
```

此时顶层配置中的 `env_list` 配置项中应将 `py312` 改为 `3.12`, `py313` 改为 `3.13`

#### 2.1.4. 其它环境配置

其它环境直接使用环境名称进行配置即可, 如:

```toml
[env.type]
description = "run type check on code base"
deps = [
    "mypy>=1.15",
]
commands = [
    ["mypy", "."],
]

[env.lint]
description = "run linting on code base"
deps = [
    "autopep8>=2.3",
    "pycln>=2.5",
]
commands = [
    ["pycln", "--config=pycln.cfg"],
    ["autopep8", "."],
]
```

上述配置对应顶层配置中 `env_list` 配置项中的 `type` 及 `lint` 值

## 3. 使用

完成上述配置后, 即可在命令行中执行如下命令:

执行所有环境命令

```bash
tox
```
