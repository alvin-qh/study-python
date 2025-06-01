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

上述命令会创建一个名为 `<project-path>` 的子目录, 并在其中生成一个 `pyproject.toml` 文件, 项目命名为 `<project-name>`

如果命令中缺省了 `--name` 参数, 则默认以 `<project-path>` 名称为项目名

### 1.2. 初始化项目

通过 `poetry init` 命令初始化项目, 在一个现有的目录中创建 `pyproject.toml` 文件

```bash
poetry init --name=<project-name>
```

上述命令会在当前目录中生成一个 `pyproject.toml` 文件, 项目命名为 `<project-name>`

如果命令中缺省了 `--name` 参数, 则默认以当前目录名称为项目名

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

添加依赖包

```bash
poetry add <package-name>
```

添加依赖包并指定版本

```bash
poetry add <package-name> == <version>
poetry add <package-name> >= <version>
```

添加本地以来包

```bash
poetry add <path-to-package>
poetry add <path-to-package> --develop
```
