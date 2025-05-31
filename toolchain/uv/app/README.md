# UV for Application

通过 UV 可以创建 Python 应用项目, 这类项目一般会直接执行, 不会进行打包, 故项目结构较 `package` 或 `lib` 类型简单

## 1. 创建项目

### 1.1. 初始化项目

在项目目录下执行以下命令

```bash
uv init --name <project_name> --app
```

之后会在项目目录下生成以下文件

```plaintext
.
├── tests
│   └── __init__.py
├── README.md
├── main.py
├── pyproject.toml
└── uv.lock
```

Application 类型的项目代码结构为 flat layout, 故没有特定的 `src` 目录, 可以按需要建立任意 `.py` 文件或任意 Python 包目录结构, 例如用于存放单元测试代码的 `tests` 包目录

### 1.2. 执行项目脚本

可通过 UV 命令执行项目相关的脚本, 包括:

```bash
uv run pytest
uv run mypy .
uv run pycln --config pyproject.toml
uv run autopep8 .
```

由于 UV 工具没有 PDM 等工具那样的 Shell 脚本定义功能, 故可通过 `invoke` 库编写脚本, 并通过如下命令执行:

```bash
uv run inv check
uv run inv start
```
