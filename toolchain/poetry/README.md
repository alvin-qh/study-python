# Poetry toolchain

Poetry 是一款现代 Python 项目管理工具, 包括项目元数据管理, 依赖管理, 构建管理, 工具配置管理等, 采用 `pyproject.toml` 文件作为项目配置文件

和功能类似的 PDM 或 UV 工具集相比较, Poetry 的功能不够全面, 执行速度较慢, 但 Poetry 出现的时间较早, 且稳定性较好, 仍被大量 Python 项目使用

## 1. 定义项目

所谓初始化项目, 即创建 `pyproject.toml` 项目文件, Poetry 具备两种方式创建 `pyproject.toml` 文件

### 1.1. 新建项目

可通过 `poetry new` 命令新建项目, 包括项目所在目录以及其中的 `pyproject.toml` 文件

```bash
poetry new <project-path> --name=<project-name>
```

如果命令中缺省了 `--name` 参数, 则默认以 `<project-path>` 名称为项目名

上述命令会创建一个名为 `<project-path>` 的子目录, 并在其中生成一个 `pyproject.toml` 文件, 项目命名为 `<project-name>`

### 1.2. 初始化项目

通过 `poetry init` 命令初始化项目, 在一个现有的目录中创建 `pyproject.toml` 文件

```bash
poetry init --name=<project-name>
```

如果命令中缺省了 `--name` 参数, 则默认以当前目录名称为项目名

上述命令会在当前目录中生成一个 `pyproject.toml` 文件, 项目命名为 `<project-name>`

### 1.3. `pyproject.toml` 文件

一个通过 Poetry 生成的 `pyproject.toml` 文件内容如下:

```toml
[project]
name = "<project-name>"
version = "0.1.0"
description = "<project-description>"
authors = [
  { name = "Alvin", email = "quhao317@163.com" },
]
license = "MIT"
readme = "README.md"
requires-python = ">=3.13,<4"
dependencies = [
  "<package1-name> >= <version>",
  "<package2-name> >= <version>",
  "<package3-name> @ file://<path-to-package>",
]

[project.optional-dependencies]
group1-name = [
  "package1-name >= <version>",
  "package2-name >= <version>",
]
group2-name = [
  "package3-name >= <version>",
  "package4-name >= <version>",
]

[tool.poetry]
package-mode = false

[tool.poetry.dependencies]
package3-name = { develop = true }

[tool.poetry.group.<group-1>.dependencies]
package1-name = "^<version>"
package2-name = "^<version>"

[tool.poetry.group.<group-2>.dependencies]
package3-name = "^<version>"
package4-name = "^<version>"

[tool.pycln]
path = "."
all = true
exclude = '\.history'

[tool.mypy]
files = [
  ".",
]
strict = true
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true
disallow_untyped_decorators = false
check_untyped_defs = true
exclude = '\.history'

[tool.autopep8]
max_line_length = 120
ignore = [
  'E501',
  'W6',
]
jobs = -1
in-place = true
recursive = true
aggressive = 3
exclude = '.history'

[tool.pytest.ini_options]
addopts = [
    '-s',
]
testpaths = [
    'tests',
]
```

### 1.3. 虚拟环境

默认情况下, Poetry 会自动管理每个项目的虚拟环境, 当在项目目录下, 通过 `poetry` 命令进行操作时 (如安装依赖, 执行 `.py` 文件等), Poetry 会自动为当前项目创建一个虚拟环境

Poetry 自动创建的虚拟环境位于 `$HOME/.cache/pypoetry/virtualenvs` 路径下, 且每个 `pyproject.toml` 文件都会自动对应该路径下的一个虚拟环境

#### 1.3.1. 自定义虚拟环境

如果不希望 Poetry 自动创建虚拟环境, 可以自己创建虚拟环境, 并通过 `poetry env use` 命令为当前项目指定虚拟环境

```bash
# 在当前项目的 .venv 目录下创建虚拟环境
python -m venv .venv --prompt=<venv-name>

# 为当前项目指定虚拟环境
poetry env use .venv/bin/python

# 在当前虚拟环境下安装 pyproject.toml 文件中定义的依赖
poetry install
```

#### 1.3.2. 管理虚拟环境

##### 查看当前项目虚拟环境

```bash
poetry env info
```

##### 列出当前项目相关的虚拟环境列表

```bash
poetry env list
```

##### 删除当前项目虚拟环境

```bash
poetry env remove <venv-name>
```

其中的 `<venv-name>` 为虚拟环境名称，可以通过 `poetry env list` 命令查看

##### 进入当前虚拟环境

可通过 `poetry env activate` 命令查看进入当前虚拟环境的命令, 例如:

```bash
poetry env activate

# 输出
source /.../bin/activate
```

将上述命令输出结果作为命令执行, 即可进入对应虚拟环境, 也可也一次性进入虚拟环境, 命令如下:

```bash
eval $(poetry env activate)
```

## 2. 管理依赖

### 2.1. 添加依赖

通过 `poetry add` 命令, 可为当前项目添加依赖包, 添加的依赖包名称及版本会记录在 `pyproject.toml` 文件 `[project]` 配置下的 `dependencies` 配置项中

#### 2.1.1. 添加依赖包

```bash
poetry add <package-name> # 如 poetry add numpy
```

依赖包添加后, 会在 `pyproject.toml` 文件 `[project]` 配置下的 `dependencies` 配置项中添加依赖包名称及版本信息, 此时依赖包的版本为最新版本

```toml
[project]
...
dependencies = [
    "<package-name> >= <version>",
]
```

#### 2.1.2. 添加依赖包并指定版本

```bash
poetry add <package-name> == <version> # 如 poetry add numpy==2.2
poetry add <package-name> >= <version> # 如 poetry add numpy>=2.2
```

同理, 该命令也会在 `pyproject.toml` 文件 `[project]` 配置下的 `dependencies` 配置项中添加依赖包名称及版本信息, 此时依赖包的版本为指定版本

```toml
[project]
...
dependencies = [
    "<package-name> == <version>",
    "<package-name> >= <version>",
]
```

#### 2.1.3. 添加本地依赖包

```bash
poetry add <path-to-package> # 如 poetry add ./libs/data-requirement
poetry add <path-to-package> --develop
```

本地依赖包添加后, 会在 `pyproject.toml` 文件 `[project]` 配置下的 `dependencies` 配置项中添加本地依赖包的路径信息

```toml
[project]
...
dependencies = [
    "<package-name> @ file:///<path-to-package>",
]
```

如果在添加依赖包时添加了 `--develop` 参数, 则依赖包会被添加为开发依赖, 此时会将本地依赖以 "可编辑依赖" 方式引入, 可以随时修改依赖包代码而无需重新安装该依赖包, 此时 `pyproject.toml` 文件内容如下:

```toml
[project]
...
dependencies = [
  "<package-name> @ file:///<path-to-package>",
]

[tool.poetry.dependencies]
<package-name> = { develop = true }
```

#### 2.1.4. 添加 URL 为依赖包

可以添加一个指向 `.whl` 文件的 URL 为依赖包, 该依赖包会从 URL 下载, 并安装到项目依赖包目录中, 命令如下:

```bash
poetry add <url-to-package> # 如 poetry add https://github.com/explosion/spacy-models/releases/download/en_core_web_trf-3.5.0/en_core_web_trf-3.5.0-py3-none-any.whl
```

或者添加一个 GIT 仓库为依赖包, 该依赖包会从 GIT 仓库中下载, 并安装到项目依赖包目录中, 命令如下:

```bash
poetry add "git+<git-repo-url>" # 如 poetry add "git+https://github.com/pypa/pip.git@22.0"
```

### 2.2. 添加开发依赖

Poetry 可以添加只在开发时需要的依赖包, 这部分依赖包在打包时不会包含在打包结果中

开发依赖必须归属于一个组, 同组的依赖项包含在 `pyproject.toml` 文件的 `[tool.poetry.group.<group-name>.dependencies]` 配置下

#### 2.2.1. 添加依赖到 `dev` 分组

默认的组名为 `dev`, 可通过如下命令添加:

```bash
poetry add pytest pytest-sugar --dev
```

该命令会在 `pyproject.toml` 文件中增加 `[tool.poetry.group.dev.dependencies]` 配置, 并在该配置下添加依赖

执行命令后 `pyproject.toml` 文件会变更如下内容:

```toml
[tool.poetry.group.dev.dependencies]
pytest = "^8.3.5"
pytest-sugar = "^1.0.0"
```

#### 2.2.2. 添加依赖到指定分组

通过 `poetry add <package-name> --group <group-name>` 命令添加依赖包到指定名称的分组中, 此命令会在 `pyproject.toml` 文件中增加 `[tool.poetry.group.<group-name>]` 配置, 并在该配置下添加依赖

要添加依赖到指定分组中, 可以使用如下命令:

```bash
poetry add pytest pytest-sugar -G/--group test
```

该命令会在 `pyproject.toml` 文件中增加 `[tool.poetry.group.test]` 配置, 并在该配置下添加依赖

执行命令后 `pyproject.toml` 文件会变更如下内容:

```toml
[tool.poetry.group.test.dependencies]
pytest = "^8.3.5"
pytest-sugar = "^1.0.0"
```

### 2.3. 添加可选依赖

当项目打包时, 其附带的可选依赖包信息也会进行打包, 但在安装程序包时, 可以选择是否安装指定的可选依赖

可选依赖必须归属于一个组, 同组的依赖项包含在 `pyproject.toml` 文件的 `[project.optional-dependencies]` 配置的指定分组名下

要添加可选依赖到指定分组, 可以使用如下命令:

```bash
poetry add click --optional cli
```

上述命令会在可选依赖下创建一个名为 `cli` 的分组, 并将依赖包添加到该分组中

执行命令后 `pyproject.toml` 文件会变更如下内容:

```toml
[project.optional-dependencies]
cli = [
  "click (>=8.2.1,<9.0.0)",
]
```

### 2.4. 锁定依赖

可生成 `poetry.lock` 文件对当前项目的依赖项进行锁定, 命令如下:

```bash
poetry lock
```

提交代码时应当将 `poetry.lock` 文件一并加入版本控制, 以保证整个团队在该项目上使用相同的依赖定义

### 2.5. 同步依赖

同步依赖的前提是当前项目已生成 `poetry.lock` 文件, 否则需先生成该文件

可通过 `poetry install` 或 `poetry sync` 命令同步依赖, 两者具备相同的功能和类似的参数, 区别在于后者会删除未在 `poetry.lock` 文件中定义的依赖

#### 2.5.1. 同步全部依赖

同步全部依赖指的是同步 `[project]` 配置下 `dependencies` 配置项中定义的依赖, 以及所有 `[tool.poetry.group.<group-name>.dependencies]` 配置项下定义的依赖, 而不包括 `[project.optional-dependencies]` 配置项中定义的依赖

命令如下:

```bash
poetry sync
```

#### 2.5.2. 同步指定依赖

可以指定只安装指定依赖, 这里的指定依赖范围为 `[project]` 配置下 `dependencies` 配置项中定义的依赖 以及 `[tool.poetry.group.<group-name>.dependencies]` 配置项下定义的依赖, 不包括 `[project.optional-dependencies]` 配置项中定义的依赖

通过如下命令可以同步指定依赖:

只同步 `[project]` 配置下 `dependencies` 配置项中定义的全部依赖

```bash
poetry sync --only main
```

只同步指定分组名称的 `[tool.poetry.group.<group-name>.dependencies]` 配置下定义的全部依赖

```bash
poetry sync --only test,lint
```

#### 2.5.3. 指定无需同步的开发依赖

可通过 `--without <group-name>` 参数来指定无需同步的 `[tool.poetry.group.<group-name>.dependencies]` 配置项下的依赖, 例如:

```bash
poetry sync --without test,lint
```

上述命令表示, `[tool.poetry.group.test.dependencies]` 以及 `[tool.poetry.group.lint.dependencies]` 配置项下的依赖将不会同步, 如果之前已经同步, 则本次同步会进行删除

#### 2.5.4. 指定同步的可选依赖

通过 `--with <group-name>` 参数来指定需要同步的 `[project.optional-dependencies]` 配置项下的依赖, 例如:

```bash
poetry sync --with cli,doc
```

上述命令表示, 在所需同步依赖的基础上, 额外增加 `[project.optional-dependencies]` 配置下的 `cli` 和 `doc` 分组中定义的依赖

## 3
