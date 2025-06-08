# PDM Toolchain

参考: <https://pdm-project.org/zh-cn/latest>

## 1. 安装 PDM

### 1.1. Linux/Mac

安装

```bash
curl -sSL https://pdm-project.org/install-pdm.py | python3 -
```

更新

```bash
pdm self update
```

卸载

```bash
curl -sSL https://pdm-project.org/install-pdm.py | python3 - --remove
```

### 1.2. Windows

安装

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://pdm-project.org/install-pdm.py | py -"
```

更新

```powershell
pdm self update
```

卸载

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://pdm-project.org/install-pdm.py | py - --remove"
```

### 1.1. 在新目录中创建项目

```bash
pdm new --name <project_name> --python <python_version/python_path> [--lib] [template] project_path
```

## 2. 新建项目

### 2.1. 安装 Python 解释器

PDM 支持安装 Python 解释器, 也可以基于系统中已有的 Python 解释器 (或 PyEnv 管理的 Python 解释器) 运行项目

安装指定版本的解释器

```bash
pdm python install 3.13t
```

删除已安装的解释器

```bash
pdm python remove 3.13t
```

列出所有通过 PDM 安装的解释器

```bash
pdm python list
```

### 2.2. 创建项目

PDM 可创建三类 Python 项目, 分别为应用 (Application), Python 库 (Lib) 以及 Python 包 (Package), 可参考:

- [Application](./app/README.md): 创建 Python 应用程序项目, 代码结构为扁平结构 (flat layout);
- [Lib](./lib/README.md): 创建 Python 库程序项目, 代码结构为 SRC 结构 (src layout);
- [Package](./package/README.md): 创建 Python 依赖包项目, 代码结构为 SRC 结构 (src layout);

PDM 创建项目后, 会在项目的根路径下生成 `pyproject.toml` 配置文件, 该文件符合 Python 的 PEP 518 标准, 该文件中管理了当前项目的基本信息, 依赖包, 工具配置, 打包构建配置等

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
    "<package1-name >= <version>",
    "<package2-name >= <version>",
]
requires-python = ">=3.13"
readme = "README.md"
license = { text = "MIT" }

[dependency-groups]
group1 = [
  "<package3-name >= <version>",
  "<package4-name >= <version>",
]
group2 = [
  "<package5-name >= <version>",
  "<package6-name >= <version>",
]

[project.optional-dependencies]
group1 = [
  "<package7-name >= <version>",
  "<package8-name >= <version>",
]
group2 = [
  "<package9-name >= <version>",
  "<package10-name >= <version>",
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

从 PyPI 仓库添加依赖包

```bash
pdm add <package-name>  # 如 pdm add numpy
pdm add <package-name==version>  # 如 pdm add numpy==2.2
pdm add <package-name>=version>  # 如 pdm add numpy>=2.2
pdm add <package-name[optional]>  # 如 pdm add requests[socks]
```

从本地或远程代码库添加依赖包

```bash
pdm add <path-to-package>  # 如 pdm add ./libs/data-requirement
pdm add <url-to-package>  # 如 pdm add https://github.com/explosion/spacy-models/releases/download/en_core_web_trf-3.5.0/en_core_web_trf-3.5.0-py3-none-any.whl
```

从 GIT 代码仓库添加依赖包

```bash
pdm add "git+<git-repo-url>" # 如 pdm add "git+https://github.com/pypa/pip.git@22.0"
pdm add "name @ git+<git-repo-url>" # 如 pdm add "pip @ git+https://github.com/pypa/pip.git@22.0"
                                    # 或 pdm add "git+https://github.com/pypa/pip.git@22.0#egg=pip"
pdm add "git+<git-repo-url#egg=<name>&subdirectory=<subpath>>" # 如 pdm add "git+https://github.com/owner/repo.git@master#egg=pkg&subdirectory=subpackage"
```

> 要对 git 使用 ssh 方案，只需将 `https://` 替换为 `ssh://git@`

### 3.2. 添加开发依赖

在 `[dependency-groups]` 中添加分组依赖, 用于当前项目开发环境依赖, 这部分依赖不会被引入到发布的软件包元数据中

```bash
pdm add <dependency> -d/--dev # 添加到 `dev` 分组中
pdm add <dependency> -dG <group-name> # 添加到指定名称的分组中
```

### 3.3. 添加可选依赖

在 `[project.optional-dependencies]` 中添加分组依赖, 这部分依赖作为当前项目的可选依赖, 可以选择性安装

```bash
pdm add <dependency> -G/--group <group-name> # 添加到指定名称的分组中
```

### 3.4. 同步依赖

同步依赖会根据 `pdm.lock` 文件中的定义, 重新为当前 Python 虚拟环境安装依赖包, 命令如下:

安装 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下所有分组中的全部依赖

```bash
pdm sync
# 或
pdm sync -dG:all
```

只安装 `[project]` 下 `dependencies` 项中定义的全部依赖, 不包含 `[dependency-groups]` 下分组中定义的依赖

```bash
pdm sync --prod/--production
```

安装 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下 `dev` 分组中定义的依赖

```bash
pdm sync -d/--dev
```

安装 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下 `group-name` 分组中定义的依赖

```bash
pdm sync -dG <group-name> # -dG 相当于 --dev --group 的组合
```

安装 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下除 `group-name` 分组外的其它分组中定义的全部依赖

```bash
pdm sync -d/--dev --without <group-name>
```

安装 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下所有分组中的全部依赖, 以及 `[project.optional-dependencies]` 下全部分组中定义的全部依赖

```bash
pdm sync -G:all/--group:all
```

安装 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下所有分组中的全部依赖, 以及 `[project.optional-dependencies]` 下 `feature-name` 分组中定义的全部依赖

```bash
pdm sync -G/--group <feature-name>
```

安装 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下所有分组中的全部依赖, 以及 `[project.optional-dependencies]` 下除 `feature-name` 分组外, 其它分组中定义的依赖

```bash
pdm sync --without <feature-name>
```

### 3.5. 同步 Lock 文件

同步 Lock 文件会根据 `pyproject.toml` 文件的定义, 重新产生 `pdm.lock` 文件

同步 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下所有分组中的全部依赖

```bash
pdm lock
# 或
pdm lock -dG:all
```

只同步 `[project]` 下 `dependencies` 项中定义的全部依赖, 不包含 `[dependency-groups]` 下分组中定义的依赖

```bash
pdm lock --prod/--production
```

同步 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下 `dev` 分组中定义的依赖

```bash
pdm lock -d/--dev
```

同步 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下 `group-name` 分组中定义的依赖

```bash
pdm lock -dG <group-name> # -dG 相当于 --dev --group 的组合
```

同步 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下除 `group-name` 分组外的其它分组中定义的全部依赖

```bash
pdm lock -d/--dev --without <group-name>
```

同步 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下所有分组中的全部依赖, 以及 `[project.optional-dependencies]` 下全部分组中定义的全部依赖

```bash
pdm lock -G:all/--group:all
```

同步 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下所有分组中的全部依赖, 以及 `[project.optional-dependencies]` 下 `feature-name` 分组中定义的全部依赖

```bash
pdm lock -G/--group <feature-name>
```

同步 `[project]` 下 `dependencies` 项中定义的全部依赖以及 `[dependency-groups]` 下所有分组中的全部依赖, 以及 `[project.optional-dependencies]` 下除 `feature-name` 分组外, 其它分组中定义的依赖

```bash
pdm lock --without <feature-name>
```

## 4. 项目安装

项目安装会完成两件工作

- 安装当前项目中全部的所需依赖;
- 如果当前项目是 `lib` 或 `package` 类型的, 则将 `src` 目录下的内容作为当前项目的可编辑依赖进行安装, 参考 `pip` 命令的 `--editable/-e` 选项

项目通过 `pdm install ...` 命令安装, 该命令的参数和 `pdm sync` 命令基本一致, 参考 [同步依赖](#34-同步依赖) 章节内容

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
pdm run main.py
```

### 6.2. 运行指定 Python 工具包

如果在当前项目的虚拟环境下安装了 Python 工具包, 那么可以通过 PDM 的 `run` 命令来运行它, 例如:

```bash
pdm run pytest

pdm run pycln --config=pyproject.toml .
pdm run mypy .
pdm run autopep8 .
```

各工具执行时, 会读取各自的配置文件, 或从 `pyproject.toml` 中读取该工具的配置, 参见 [配置 Python 工具](#5-配置-python-工具) 章节

### 6.3. 指定运行脚本

可以通过 `pyproject.toml` 中的 `[tool.pdm.scripts]` 配置项来设置运行脚本, 并通过 `pdm run <script_name>` 来运行指定的脚本, 例如:

```toml
[tool.pdm.scripts]
start = "main.py"
check = { composite = [
  "pycln --config=pyproject.toml .",
  "mypy .",
  "autopep8 ."
] }
test = "pytest"
clean = { call = "clear:main" }
```

上述脚本可通过如下命令运行:

```bash
pdm run start
pdm run check
pdm run test
pdm run clean
```

## 7. 打包构建

对于类型为 `lib` 或 `package` 的项目, 可打包为 `.tar.gz` 或 `.whl` 文件, 以便安装在其它环境中

### 7.1. 配置打包构建器

在 `pyproject.toml` 中增加如下配置:

```toml
[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"
```

PDM 支持多种打包器, `pdm-backend` 是 PDM 的默认打包器, 此外, 诸如 `setuptools`, `hatchling` 等打包器也可以使用

默认情况下, PDM 只打包 `src` 目录下的文件, 如果需要打包其他目录下的文件 (或排除某些文件), 或包含指定源文件, 可以在 `pyproject.toml` 文件中添加如下配置:

```toml
[tool.pdm.build]
includes = [
  "package/",
  "clear.py",
]
excludes = [
  "**/__pycache__/",
]
source-includes = [
  "scripts/",
  "tests/"
]
```

也可以指定非 `src` 目录作为源代码目录:

```toml
[tool.pdm.build]
package-dir = "my_src"
```

可通过如下命令进行打包

```bash
pdm build
```

打包结果存储在 `dist` 目录中生成一个 `.tar.gz` 文件和一个 `.whl` 文件

### 7.2. 指定启动脚本

对于 `package` 类型的项目, 安装包后, 会提供一个执行入口, 用于启动项目, 需要在 `pyproject.toml` 文件中添加如下配置:

```toml
[project.scripts]
pdm-package = "pdm_package:run"
```

表示当前项目的执行入口, 当项目打包产生的 `.whl` 文件被安装后, 可通过项目名称直接运行

## 8. 导入导出 PIP 格式依赖文件

### 8.1. 导出 `requirements.txt` 文件

PDM 支持将当前项目 `pyproject.toml` 文件中引入的依赖导出为 `requirements.txt` 文件, 以便之后通过 `pip` 命令安装依赖, 具体命令为:

```bash
pdm export -dG:all --no-hashes -f/--format requirements > requirements.txt
```

上述命令表示导出当前项目 `pyproject.toml` 中包含的所有依赖, 包括:

- `[project]` 配置下 `dependencies` 配置项中定义的依赖
- `[dependency-groups]` 配置下所有分组中的依赖 (`-dG:all` 选项)
- `[project.optional-dependencies]` 配置下所有分组中的依赖 (`-dG:all` 选项)
- 导出为 `requirements.txt` 文件 (`-f/--format requirements` 选项)

PDM 可以导出多种格式的依赖文件, 通过 `-f/--format` 选项指定, 参考 `pdm export --help` 帮助信息

### 8.2. 导入 `requirements.txt` 文件

PDM 支持将 `requirements.txt` 文件导入为 `pyproject.toml` 文件, 以便之后通过 PDM 安装依赖, 具体命令为:

```bash
pdm import -f/--format requirements requirements.txt
```

PDM 可以导入多种格式的依赖文件, 通过 `-f/--format` 选项指定, 参考 `pdm import --help` 帮助信息

PDM 也可以将 `requirements.txt` 文件中的依赖导入到当前项目 `pyproject.toml` 文件的特定依赖分组中, 参考 `pdm import` 命令的 `--dev` 和 `--group` 选项
