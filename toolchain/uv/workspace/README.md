# Workspace

所谓 Workspace, 可以认为是依赖库的一种统一管理模式, 和独立的库相比, Workspace 模式可以

- 统一管理项目, 即可以在一个目录下管理主项目和其依赖的库项目
- 统一管理虚拟环境, 即主项目和其依赖的库项目使用相同的 Python 虚拟环境, 从而统一管理所有项目的依赖

## 1. 设置 Workspace

本例中, 整个 Workspace 的目录结构如下:

```plaintext
.
├── packages
│   ├── lib
│   │   ├── src
│   │   │   └── uv_workspace_lib
│   │   │       ├── __init__.py
│   │   │       └── py.typed
│   │   ├── tests
│   │   │   └── __init__.py
│   │   ├── pyproject.toml
│   │   └── README.md
│   └── utils
│       ├── src
│       │   └── uv_workspace_utils
│       │       ├── __init__.py
│       │       └── py.typed
│       ├── tests
│       │   └── __init__.py
│       ├── pyproject.toml
│       └── README.md
├── tests
│   └── __init__.py
├── clear.py
├── main.py
├── pyproject.toml
├── README.md
├── tasks.py
└── uv.lock
```

这里的目录结构展示了一整个 Workspace, 其中:

- 项目根目录下的 `pyproject.toml` 文件用来配置根项目以及整个 Workspace 的配置
- `packages` 目录下的各子目录下的 `pyproject.toml` 文件用来配置 Workspace 下的子项目

### 1.1. 配置主项目

主项目一般位于项目根目录下, 通过 `pyproject.toml` 文件来配置主项目, 该配置和一般配置类似, 只是多了一个 `[tool.uv.workspace]` 配置项, 该配置项用来配置 Workspace 的配置, 包括:

```toml
[tool.uv.workspace]
members = [
    "packages/*",
]
exclude = []
```

上述配置表示:

- `members`: 为一个数组类型, 表示 Workspace 的成员, 数组中的元素为要包含为子项目的路径, 可以使用通配符来匹配多个路径
- `exclude`: 为一个数组类型, 表示从 Workspace 中排除的项, 数组中的元素为要排除的路径, 可以使用通配符来匹配多个路径

本例中配置表示, 将 `packages/lib` 和 `packages/utils` 作为 Workspace 的成员, 并且不排除任何子项目

### 1.2. 配置子项目

当主项目的 `pyproject.toml` 文件中配置了 `[tool.uv.workspace]` 后, 即可在添加子项目

#### 1.2.1. 创建子项目

按照本例的配置, 在 `packages` 目录下创建 `lib` 和 `utils` 两个子项目目录

在各子项目目录下执行创建项目命令

```bash
# 在 `packages/lib` 目录下创建项目
uv init --name uv-workspace-lib --lib

# 在 `packages/utils` 目录下创建项目
uv init --name uv-workspace-utils --lib
```

即通过 UV 在 `packages` 目录下创建 `lib` 类型项目, 作为主项目的依赖库

注意: 如果主项目需要打包, 则子项目也必须配置打包构建的配置, 否则主项目无法正确打包, 即在各个子项目的 `pyproject.toml` 文件中添加如下配置:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

更多关于打包器说明, 请参见 [配置打包器](../README.md#71-配置打包器)

#### 1.2.2. 关联子项目

主项目需要将子项目添加为依赖, 具体方法如下:

```bash
uv add packages/lib
uv add packages/utils
```

此时会在主项目的 `pyproject.toml` 文件中添加如下如下配置:

```toml
[project]
...
dependencies = [
    "uv-workspace-lib",
    "uv-workspace-utils",
]

[tool.uv.sources]
uv-workspace-lib = {workspace = true}
uv-workspace-utils = {workspace = true}
```

即表示将 Workspace 下的子项目作为主项目依赖进行管理

子项目被作为主项目的 “可编辑” 依赖, 所以当子项目代码修改后, 无需在主项目中更新依赖, 主项目即可使用到最新的子项目依赖

> 可编辑依赖包参见 `pip` 的 `--editable` (或 `-e`) 参数说明

## 2. 使用子项目

### 2.1. 主项目引用子项目

正常情况下, 将子项目看作是主项目的依赖, 在主项目中正常引用即可

### 2.2. 针对子项目的 UV 命令

可以进入子项目目录, 通过 UV 命令对子项目进行操作, 就和操作普通项目完全一致

但如果想在主项目下运行子项目, 可以通过 `uv` 命令的 `--package` 参数指定子项目名称, 例如:

```bash
uv add --package uv-workspace-lib mypy mypy-extensions --group type
```

上述命令相当于在 `./packages/uv-workspace-lib` 目录下运行：

```bash
uv add mypy mypy-extensions --group type
```

### 2.3. 执行子项目工具或脚本

可以在主项目目录下执行子项目相关的工具或脚本, 例如为子项目执行单元测试或代码检查

UV 命令参数 `--package` 无法在执行子项目工具或脚本的场景下生效, 需要使用 `--directory` 参数指定子项目目录, 即要运行工具或脚本的目录,  例如:

```bash
uv run mypy # 执行主项目下的 mypy 工具
uv run --directory packages/lib mypy # 执行子项目下的 mypy 工具
```

参考 [tasks.py](./tasks.py) 文件中列举的 UV 命令
