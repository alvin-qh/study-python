# UV for lib

通过 UV 可以创建 Python 库项目, 用于编译一个 Python 库, 输出 `.whl` 文件供其它 Python 项目

## 1. 创建项目

### 1.1. 创建项目文件夹

```bash
mkdir <project_name>
```

### 1.2. 初始化项目

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

uv 会在项目中创建 `src` 目录, 所有的项目源代码都应位于 `src` 目录下, 且 `src` 目录下必须具备一个和项目名相同的包 (本例中为 `uv_lib` 包), 作为当前 Python 库的根包名

对于 `lib` 类型项目, `uv` 会将 `src` 目录下的内容作为 "可编辑" 依赖安装到当前的虚拟环境中 (即 `.venv` 目录)

> 可编辑依赖包参见 `pip` 的 `--editable` (或 `-e`) 参数说明

项目中的 `pyproject.toml` 文件定义了项目的配置项, 包括:

#### 1.2.1. 项目配置

```toml
[project]
name = "<project_name>"
version = "0.1.0"
description = "Project Description"
readme = "README.md"
authors = [
    { name = "Alvin", email = "quhao317@163.com" },
]
requires-python = ">=3.13"
dependencies = []
```

其中 `dependencies` 配置项定义了项目的依赖包

#### 1.2.2. 可选依赖包

可选依赖包指的是只在开发时会用到的依赖包, 在生产环境中无需安装, 此类依赖包可以添加到 `dependency-groups` 分组下:

```toml
[dependency-groups]
dev = []
lint = [
    "autopep8>=2.3.2",
    "mypy>=1.15.0",
]
test = [
    "pytest>=8.3.5",
]
```

uv 有一个默认的 `dev` 分组, 表示仅在开发时用到的包, 也可以在安装依赖包的时候指定其它分组

#### 1.2.3. 配置工具链

##### `pytest` 配置

```toml
[tool.pytest.ini_options]
addopts = [
    '-vvs',
]
testpaths = [
    'tests',
]
```

其它配置项参见: <https://docs.pytest.org/en/7.1.x/reference/customize.html>

##### `pycln` 配置

```toml
[tool.pycln]
all = true
```

其它配置参见参见: <https://hadialqattan.github.io/pycln/#/?id=usage>

##### `mypy` 配置

```toml
[tool.mypy]
strict = true
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true
disallow_untyped_decorators = false
check_untyped_defs = true
exclude = ['^.venv\.py$', '^.test\.py$']
```

其它配置参见: <https://mypy.readthedocs.io/en/stable/config_file.html>

##### `autopep8` 配置

```toml
[tool.autopep8]
max_line_length = 120
ignore = ['E501', 'W6']
in-place = true
recursive = true
jobs = -1
aggressive = 3
```

其它配置项参见: <https://github.com/hhatto/autopep8?tab=readme-ov-file#configuration>

#### 1.2.4. 配置打包构建器

打包构建器用于将当前项目打包为 `.whl` 文件, 可上传到 `PyPI` 仓库中供其它项目使用

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

可通过如下命令进行打包

```bash
uv build
```

打包结果存储在 `dist` 目录中

## 2. 依赖管理

uv 通过创建 `virtualenv` 虚拟环境来管理依赖, 每个项目都有一个独立的虚拟环境, 通过 uv 命令对虚拟环境进行管理

另外, uv 还会创建 `uv.lock` 文件, 用于对当前项目的依赖进行锁定, 确保项目在不同的机器上运行时, 依赖包的版本一致

### 2.1. 添加依赖

可通过 `uv add` 命令添加项目依赖包

```bash
uv add <package_name>
```

或通过

```bash
uv remove <package_name>
```

删除已安装的依赖包

安装或删除的依赖位于 `pyproject.toml` 文件的 `[project]` 节点下的 `dependencies` 数组项中

### 2.2. 添加依赖到分组

如要将依赖安装到 `pyproject.toml` 文件中 `[dependency-groups]` 配置项的 `dev` 分组下, 可执行如下命令:

```bash
uv add pytest pycln mypy autopep8 --dev
```

如要将依赖安装到 `pyproject.toml` 文件中 `[dependency-groups]` 配置项的指定分组下, 可执行如下命令:

```bash
uv add pytest --group test
uv add pycln mypy autopep8 --group lint
```

要删除指定分组内的依赖包, 需要通过 `remove` 命令:

```bash
uv remove pytest pycln mypy autopep8 --dev
uv remove pytest --group test
uv remove lint pycln mypy autopep8 --group lint
```

### 2.3. 同步依赖

执行如下命令可以根据 `pyproject.toml` 文件中的依赖项, 重新生成 `.venv` 目录中安装的依赖项目, 更新 Python 虚拟环境

```bash
uv sync [--group <group> --no-group <group> --no-default-group --all-groups --only-group <group>]
uv sync [-U -v -i https://pypi.tuna.tsinghua.edu.cn/simple]
```

### 2.4. 同步 `uv.lock` 文件

执行如下命令可以根据 `pyproject.toml` 文件中的依赖项, 重新生成 `uv.lock` 文件

```bash
uv lock [-U -v -i https://pypi.tuna.tsinghua.edu.cn/simple]
```

## 3. 执行 Python 脚本

uv 可以直接执行当前项目中的任意 `.py` 文件或当前项目虚拟环境下安装的任意 Python 工具包 (例如 `pytest`)

### 3.1. 运行指定的 `.py` 文件

可以通过 uv 的 `run` 命令来运行项目中指定的 `.py` 文件, 例如:

```bash
uv run main.py
```

### 3.2. 运行指定 Python 工具包

如果在当前项目的虚拟环境下安装了 Python 工具包, 那么可以通过 uv 的 `run` 命令来运行它, 例如:

```bash
uv run pytest

uv run pycln .
uv run mypy .
uv run autopep8 .
```

各工具执行时, 会读取各自的配置文件, 或从 `pyproject.toml` 中读取该工具的配置, 参见 [配置工具链](#123-配置工具链)
