# UV Toolchain

参考: <https://pdm-project.org/zh-cn/latest>

## 1. 安装 UV

### 1.1. Linux/Mac

安装

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

更新

```bash
uv self update
```

卸载

```bash
# 清除缓存
uv cache clean
rm -r "$(uv python dir)"
rm -r "$(uv tool dir)"

# 删除 uv
rm ~/.local/bin/uv ~/.local/bin/uvx
```

### 1.2. Windows

安装

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

更新

```powershell
uv self update
```

```bash
# 清除缓存
uv cache clean
rm -Recurse -Force "$(uv python dir)"
rm -Recurse -Force "$(uv tool dir)"

# 删除 uv
rm $HOME\.local\bin\uv.exe
rm $HOME\.local\bin\uvx.exe
```

## 2. 新建项目

### 2.1. 安装 Python 解释器

UV 支持安装 Python 解释器, 也可以基于系统中已有的 Python 解释器 (或 PyEnv 管理的 Python 解释器) 运行项目

安装最新版本的 Python 解释器

```bash
uv python install
```

安装指定版本的 Python 解释器

```bash
uv python install 3.13

# 或者一次安装多个版本的 Python 解释器
uv python install 3.13 3.13t
```

或者安装其它 Python 解释器

```bash
uv python install pypy@3.10
```

重新安装 Python 解释器

```bash
uv python install --reinstall
```

删除已安装的解释器

```bash
uv python uninstall 3.13t
```

列出所有通过 uv 安装的 Python 解释器

```bash
uv python list
```

查看某个版本的解释器安装位置

```bash
uv python find 3.13
```

### 2.2. 创建项目

UV 可创建三类 Python 项目, 分别为应用 (Application), Python 库 (Lib) 以及 Python 包 (Package), 可参考:

- [Application](./app/README.md): 创建 Python 应用程序项目, 代码结构为扁平结构 (flat layout);
- [Lib](./lib/README.md): 创建 Python 库程序项目, 代码结构为 SRC 结构 (src layout);
- [Package](./package/README.md): 创建 Python 依赖包项目, 代码结构为 SRC 结构 (src layout);

UV 创建项目后, 会在项目的根路径下生成 `pyproject.toml` 配置文件, 该文件符合 Python 的 PEP 518 标准, 该文件中管理了当前项目的基本信息, 依赖包, 工具配置, 打包构建配置等

一个典型的 `pyproject.toml` 文件内容如下:

```toml
[project]
name = "<project-name>"
version = "1.0.0"
description = "<project-description>"
authors = [
    { name = "Alvin", email = "quhao317@163.com" },
]
dependencies = [
    "<package1>=1.0",
    "<package2>=2.0",
    "<package3>=2.2",
]
requires-python = ">=3.13"
readme = "README.md"
license = { text = "MIT" }

[dependency-groups]
group1 = [
  "<group1-dependency1>=1.0>"
  "<group1-dependency2>=2.0>"
]
group2 = [
  "<group2-dependency1>=2.0>"
  "<group2-dependency2>=3.0>"
]

[project.optional-dependencies]
feature1 = [
    "<feature1-package1>=2.0>",
    "<feature1-package2>=3.1>",
]
feature2 = [
    "<feature2-package1>=2.0>",
    "<feature2-package2>=1.1>",
]

[tool.pdm.scripts]
start = "main.py"
check = { composite = [
    "pycln --config=pyproject.toml .",
    "mypy .",
    "autopep8 ."
] }
test = "pytest"
clean = { call = "clear:main" }

[tool.pycln]
all = true
exclude = '\.history'

[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true
disallow_untyped_decorators = false
check_untyped_defs = true
exclude = [
    '.venv',
    '.history',
]

[tool.autopep8]
max_line_length = 120
ignore = ['E501', 'W6']
in-place = true
recursive = true
jobs = -1
aggressive = 3

[tool.pytest.ini_options]
addopts = [
    '-vvs',
]
testpaths = [
  'tests',
]
```

其中:

- `[project]`: 用于配置项目的基本信息, 包括项目名称, 版本号, 所依赖 Python 解释器版本, 授权证书以及项目依赖包；
- `[dependency-groups]`: 配置项目在开发时相关的依赖包, 以分组方式管理, 该配置项下的依赖包不会进行打包分发;
- `[project.optional-dependencies]`: 当前项目的可选依赖包, 通过添加不同的可选依赖包, 可以让项目具备不同功能;
- `[tool.xxx]`: 工具配置, 包括打包工具, 测试工具, 代码检测工具, 代码管理工具等;

## 3. 依赖管理

### 3.1. 添加依赖

在 `[project]` 的 `dependencies` 项中添加依赖, 用于当前项目的生产环境依赖

#### 3.1.1. 添加 PyPI 仓库中的依赖

```bash
uv add <package-name>  # 如 uv add numpy
uv add <package-name> -i https://pypi.tuna.tsinghua.edu.cn/simple # 添加依赖到指定源
uv add <package-name> -U # 升级依赖

uv add <package-name==version>  # 如 uv add numpy==2.2
uv add <package-name>=version>  # 如 uv add numpy>=2.2
uv add <package-name[optional]>  # 如 uv add requests[socks]
```

可通过 `UV_DEFAULT_INDEX` 环境变量来指定 PyPI 镜像地址

```bash
export UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 3.1.2. 添加本地 Python 代码作为依赖

```bash
uv add <path-to-package> # 如 uv add ./libs/data-requirement
uv add <url-to-package> # 如 uv add https://github.com/explosion/spacy-models/releases/download/en_core_web_trf-3.5.0/en_core_web_trf-3.5.0-py3-none-any.whl
```

此时会在 `pyproject.toml` 文件的 `[project]` 节点下的 `dependencies` 数组项中添加本地依赖包, 并通过 `[tool.uv.sources]` 节点来指定该依赖包的源码路径

```toml
[project]
...
dependencies = [
  "uv-lib",
]

[tool.uv.sources]
uv-lib = { path = "../lib" }
```

#### 3.1.3. 添加 GIT 代码仓库为依赖

```bash
uv add "git+<git-repo-url>" # 如 uv add "git+https://github.com/pypa/pip.git@22.0"
```

> 要对 git 使用 ssh 方案，只需将 `https://` 替换为 `ssh://git@`

#### 3.1.4. 添加 requirements.txt 文件中的依赖

```bash
uv add -r requirements.txt -c constraints.txt # 添加 requirements.txt 中的全部依赖
```

### 3.2. 添加开发依赖

在 `[dependency-groups]` 中添加分组依赖, 用于当前项目开发环境依赖, 这部分依赖不会被引入到发布的软件包元数据中

```bash
uv add <package-name> --optional <group-name> # 添加到 `dev` 分组中
uv add <package-name> --group <group-name> # 添加到指定名称的分组中
```

### 3.3. 添加可选依赖

在 `[project.optional-dependencies]` 中添加分组依赖, 这部分依赖作为当前项目的可选依赖, 可以选择性安装

```bash
uv add <package-name> --optional <group-name> # 添加到指定名称的分组中
```

### 3.4. 移除依赖

移除依赖, 命令如下:

```bash
uv remove <package-name> # 移除指定名称的依赖项
uv remove <package-name> --group <group-name> # 移除开发依赖下指定分组的依赖项
uv remove <package-name> --optional <group-name> # 移除可选依赖下指定分组的依赖项
```

### 3.5. 同步依赖

同步依赖会根据 `uv.lock` 文件中的定义, 重新为当前 Python 虚拟环境安装依赖包, 命令如下:

安装 `[project]` 下 `dependencies` 项中定义的全部依赖

```bash
uv sync

```

安装 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下所有分组中的全部依赖

```bash
uv sync --all-groups
```

只安装 `[project]` 下 `dependencies` 项中定义的全部依赖, 不包含 `[dependency-groups]` 下 `dev` 分组中定义的依赖

```bash
uv sync --no-dev
```

安装 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下 `dev` 分组中定义的依赖

```bash
uv sync --only-dev
```

安装 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下 `group-name` 分组中定义的依赖

```bash
uv sync --group <group-name>
```

安装 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下除 `group-name` 分组外的其它分组中定义的全部依赖

```bash
uv sync --no-group <group-name>
```

安装 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下所有分组中的全部依赖, 以及 `[project.optional-dependencies]` 下全部分组中定义的全部依赖

```bash
uv sync --all-extras
```

安装 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下所有分组中的全部依赖, 以及 `[project.optional-dependencies]` 下 `feature-name` 分组中定义的全部依赖

```bash
uv sync --extra <feature-name>
```

安装 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下所有分组中的全部依赖, 以及 `[project.optional-dependencies]` 下除 `feature-name` 分组外, 其它分组中定义的依赖

```bash
uv sync --no-extra <feature-name>
```

如果当前项目类型为 `lib` 或 `app`, 则 `uv sync` 也会将当前项目本身作为可编辑依赖项 (editable package) 安装到当前 Python 虚拟环境中, 参考 `pip` 命令的 `--editable/-e` 选项

### 3.6. 同步 Lock 文件

同步 Lock 文件会根据 `pyproject.toml` 文件的定义, 重新产生 `uv.lock` 文件

```bash
uv lock
```

## 4. 配置打包

打包构建器用于将当前项目打包为 `.whl` 文件, 可上传到 `PyPI` 仓库中供其它项目使用

### 4.1. 配置打包器

UV 支持多种打包器, 包括 `setuptools`, `hatchling` 和 `uv_build`, 默认使用 `hatchling` 打包器, 可通过在 `pyproject.toml` 文件中添加 `[build-system]` 配置项来配置打包器

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

可以在初始化项目时通过 `uv init --backend <backend-name>` 命令指定打包器, 命令如下:

```bash
uv init --name uv-build-demo --app --backend hatchling
```

### 4.2. 配置打包器参数

可以通过在 `pyproject.toml` 文件中添加 `[tool.uv.build-backend]` 配置项来配置打包器参数

```toml
[tool.uv.build-backend]
module-root = "<module-root-path>"
module-name = "<module-name>"
default-excludes = false
source-exclude = [
  "tests/**",
  ...,
]
wheel-exclude = [
  "*.bin",
  ...,
]
data = [
  "scripts": "<script-path>",
  "data": "<data-path>",
  "headers": "<headers-path>",
]
```

其中:

- `module-root`: 要打包的模块根路径, 默认为 `src` 目录 (src layout) 或为空字符串表示项目根路径 (flat layout)
- `module-name`: 要打包的模块目录名, 即 `module-root` 下的子目录名
- `default-excludes`: 是否排除默认的文件或目录, 默认为 `True`, 默认排除 `__pycache__`, `*.pyc` 以及 `*.pyo` 目录和文件
- `source-exclude`: 当打包源代码时, 要排除的源文件或目录 (打包源代码即打包为 `.tar.gz` 包)
- `wheel-exclude`: 当打包 wheel 包时, 要排除的源文件或目录
- `data`: 通过 wheel 包安装时, 自动安装的文件, 包括:
  - `scripts`: 脚本文件目录, 该目录下的内容会自动安装到当前虚拟环境的 `bin` 目录下 (即 `<venv>/bin` 下), 可直接执行
  - `data`: 数据文件目录, 该目录下的内容复制到当前虚拟环境的的根目录下 (即 `<venv>/` 下)
  - `headers`: 头文件目录, 该目录下的内容会复制到当前系统的头文件m目录下 (对于 Linux, 即 `/usr/include` 下)

### 4.3. 执行打包

可通过如下命令进行打包

```bash
uv build
```

打包后会在 `dist` 目录下生成 `.whl` 文件以及 `.tar.gz` 文件

## 5. 配置 Python 工具

可以通过 `pyproject.toml` 文件取代很多 Python 工具的配置文件, 例如 `pytest` 工具的 `pytest.ini` 文件, 可通过在 `pyproject.toml` 文件中添加 `[tool.pytest.ini_options]` 配置项取代

具体工具配置, 可参考该工具的相关文档

### 5.1. pytest 配置

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

### 5.2. pycln 配置

```toml
[tool.pycln]
all = true
exclude = '\.history'
```

其它配置参见参见: <https://hadialqattan.github.io/pycln/#/?id=usage>

### 5.3. mypy 配置

```toml
[tool.mypy]
strict = true
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true
disallow_untyped_decorators = false
check_untyped_defs = true
exclude = [
  '.venv',
  '.history',
]
```

其它配置参见: <https://mypy.readthedocs.io/en/stable/config_file.html>

### 5.4. autopep8 配置

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

## 6. 执行项目脚本

PDM 可以直接执行当前项目中的任意 `.py` 文件或当前项目虚拟环境下安装的任意 Python 工具包 (例如 `pytest`)

### 6.1. 运行指定的 Python 文件

可以通过 PDM 的 `run` 命令来运行项目中指定的 Python 文件, 例如:

```bash
uv run main.py
```

### 6.2. 运行指定 Python 工具包

如果在当前项目的虚拟环境下安装了 Python 工具包, 那么可以通过 UV 的 `run` 命令来运行它, 例如:

```bash
uv run pytest
uv run pycln --config=pyproject.toml
uv run mypy .
uv run autopep8 .
```

各工具执行时, 会读取各自的配置文件, 或从 `pyproject.toml` 中读取该工具的配置, 参见 [配置 Python 工具](#5-配置-python-工具) 章节

### 6.3. 指定启动脚本

对于 `package` 类型的项目, 安装包后, 会提供一个执行入口, 用于启动项目, 需要在 `pyproject.toml` 文件中添加如下配置:

```toml
[project.scripts]
pdm-package = "pdm_package:run"
```

表示当前项目的执行入口, 当项目打包产生的 `.whl` 文件被安装后, 可通过项目名称直接运行

## 7. PIP 兼容

UV 支持 PIP 兼容命令, 包括导出 `requirements.txt` 文件, 安装依赖, 卸载依赖等

### 7.1. 导出 `requirements.txt` 文件

```bash
uv export --all-groups --no-hashes --no-editable --format requirements.txt > requirements.txt
```

也可以通过 `uv pip` 命令

```bash
uv pip freeze > requirements.txt
```

### 7.2. 安装依赖

可以通过 PIP 兼容命令, 在当前项目虚拟环境中安装依赖, 包括:

```bash
uv pip install mypy mypy-extensions
```

也可以通过 `requirements.txt` 文件批量安装依赖

```bash
uv pip install -r/--requirement requirements.txt
```

包括从本地安装依赖, 并将其安装为可编辑依赖包

```bash
uv pip install -e/--editable ./src
```

### 7.3. 卸载依赖

可以通过 PIP 兼容命令, 在当前项目虚拟环境中卸载依赖, 包括:

 ```bash
uv pip uninstall mypy mypy-extensions
```

也可以通过 `requirements.txt` 文件批量卸载依赖

```bash
uv pip uninstall -r/--requirement requirements.txt
```

### 7.4. 查看依赖

通过 PIP 兼容命令, 在当前项目虚拟环境中查看依赖, 包括:

通过 `tabular` 格式查看所有依赖

```bash
uv pip list
```

通过 `requirements` 格式查看所有依赖

```bash
uv pip freeze
```

查看依赖关系树形结构

```bash
uv pip tree
```

查看某个具体依赖包

```bash
uv pip show mypy
```

### 7.5. 校验依赖

通过 PIP 兼容命令, 可以校验当前项目虚拟环境中依赖的正确性:

```bash
uv pip check
```
