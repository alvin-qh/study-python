# UV for package

通过 UV 可以创建 Python 可执行包项目, 用于编译一个可执行的 Python 包, 输出 `.whl` 文件并在安装后执行

## 1. 创建项目

### 1.1. 初始化项目

在项目目录下执行以下命令

```bash
uv init --name <project_name> --package
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

UV 会在项目中创建 `src` 目录, 所有的项目源代码都应位于 `src` 目录下, 且 `src` 目录下必须具备一个和项目名相同的包 (本例中为 `uv_package` 包), 作为当前 Python 库的根包名

对于 `package` 类型项目, `uv` 会将 `src` 目录下的内容作为 "可编辑" 依赖安装到当前的虚拟环境中 (即 `.venv` 目录)

> 可编辑依赖包参见 `pip` 的 `--editable` (或 `-e`) 参数说明

### 1.2. 配置包启动脚本

对于可执行 Python 包, 需要配置一个启动脚本, 用于指定启动该包主程序的入口

```toml
[project.scripts]
uv-package = "uv_package:run"
```

脚本名一般和当前项目的名称一致, 后面指定启动该项目的入口函数, 本例中为 `src/uv_package` 包导出的 `run` 函数

## 2. 执行 Python 脚本

UV 可以直接执行当前项目中的任意 `.py` 文件或当前项目虚拟环境下安装的任意 Python 工具包 (例如 `pytest`)

### 2.1. 运行指定的 `.py` 文件

可以通过 UV 的 `run` 命令来运行项目中指定的 `.py` 文件, 例如:

```bash
uv run main.py
```

### 2.2. 运行指定 Python 工具包

如果在当前项目的虚拟环境下安装了 Python 工具包, 那么可以通过 UV 的 `run` 命令来运行它, 例如:

```bash
uv run pytest

uv run mypy .
uv run pycln --config=pyproject.toml
uv run autopep8 .
```

各工具执行时, 会读取各自的配置文件, 或从 `pyproject.toml` 中读取该工具的配置, 参见 [配置 Python 工具](../README.md#5-配置-python-工具)

由于 UV 工具没有 PDM 等工具那样的 Shell 脚本定义功能, 故可通过 `invoke` 库编写脚本, 并通过如下命令执行:

```bash
uv run inv check
```

## 3. 打包构建

通过以下命令可以将当前项目打包为 `.whl` 文件以及 `.tar.gz` 文件

```bash
uv build
```

命令执行完毕后, 会在 `dist` 目录中生成 `uv_package-0.1.0-py3-none-any.whl` 文件

该文件可通过 `pip install` 命令安装到其它项目环境中

```bash
pip install uv_package-0.1.0-py3-none-any.whl
```

安装完毕后, 即可通过启动脚本启动项目

```bash
uv-package
```

UV 打包相关配置参考 [配置打包](../README.md#4-配置打包)

参见 [配置包启动脚本](#12-配置包启动脚本) 了解如何定义程序执行入口
