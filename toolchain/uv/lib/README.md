# UV for lib

通过 UV 可以创建 Python 库项目, 用于编译一个 Python 库, 输出 `.whl` 文件和 `.tar.gz` 文件供其它 Python 项目引用

## 1. 创建项目

### 1.1. 初始化项目

在项目目录下执行以下命令

```bash
uv init --name <project_name> --lib
```

之后会在项目目录下生成以下文件

```plaintext
.
├── src
│   └── <project_name>
│       ├── __init__.py
│       └── py.typed
├── tests
│   └── __init__.py
├── README.md
├── pyproject.toml
└── uv.lock
```

UV 会在项目中创建 `src` 目录, 所有的项目源代码都应位于 `src` 目录下, 且 `src` 目录下必须具备一个和项目名相同的包 (本例中为 `uv_lib` 包), 作为当前 Python 库的根包名

对于 `lib` 类型项目, UV 会将 `src` 目录下的内容作为 "可编辑" 依赖安装到当前的虚拟环境中 (即 `.venv` 目录)

> 可编辑依赖包参见 `pip` 的 `--editable` (或 `-e`) 参数说明

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
```

## 2. 打包构建

通过以下命令可以将当前项目打包为 `.whl` 文件以及 `.tar.gz` 文件

```bash
uv build
```

命令执行完毕后, 会在 `dist` 目录中生成 `uv_lib-0.1.0-py3-none-any.whl` 文件

该文件可通过 `pip install` 命令安装到其它项目环境中

```bash
pip install uv_lib-0.1.0-py3-none-any.whl
```

参考 [配置打包](../README.md#4-配置打包)
