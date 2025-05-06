# PDM for Package

通过 PDM 可以创建 Python 可执行包项目, 用于编译一个可执行的 Python 包, 输出 `.whl` 文件并在安装后执行

## 1. 创建项目

### 1.1. 创建项目文件夹

```bash
mkdir <project_name>
```

### 1.2. 初始化项目

在项目目录下执行以下命令

```bash
pdm init
```

此时 PDM 会提示一系列交互式问题, 其中

```plaintext
Do you want to build this project for distribution(such as wheel)?
If yes, it will be installed by default when running `pdm install`. [y/n] (n):
```

该问题选择为 `y`, 表示当前项目具备构建配置, 可以打包生成 `.whl` 文件

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
└── pdm.lock
```

PDM 会在项目中创建 `src` 目录, 所有的项目源代码都应位于 `src` 目录下, 且 `src` 目录下必须具备一个和项目名相同的包 (本例中为 `pdm_package` 包), 作为当前 Python 库的根包名

对于 `package` 类型项目, PDM 会将 `src` 目录下的内容作为 "可编辑" 依赖安装到当前的虚拟环境中 (即 `.venv` 目录)

> 可编辑依赖包参见 `pip` 的 `--editable` (或 `-e`) 参数说明

项目中的 `pyproject.toml` 文件定义了项目的配置项, 包括:

#### 1.2.1. 项目配置

```toml
[project]
name = "<project_name>"
version = "0.1.0"
authors = [
  { name = "Alvin", email = "quhao317@163.com" }
]
dependencies = []
requires-python = ">=3.13"
license = { text = "MIT" }

[tool.pdm]
distribution = true
```

其中:

- `[project]` 节点的 `dependencies` 配置项定义了项目的依赖包
- `[tool.pdm]` 节点的 `distribution` 配置项表示当前项目是否需要进行构建 (如构建为 `.whl` 文件), `true` 表示需要构建

#### 1.2.2. 可选依赖包

可选依赖包指的是只在开发时会用到的依赖包, 在生产环境中无需安装,

PDM 支持两种可选依赖包的配置方式:

1. 通过 `--dev` 参数来添加可选依赖包, 该方法会将依赖包安装到 `pyproject.toml` 文件中 `[dependency-groups]` 节点的 `dev` 分组下, 例如:

   ```bash
   pdm add pytest --dev
   ```

   会在 `pyproject.toml` 文件中添加如下内容:

   ```toml
   [dependency-groups]
   dev = [
       "pytest>=8.3.5",
   ]
   ```

2. 通过 `--group` 参数来添加可选依赖包, 该方法会将依赖包安装到 `pyproject.toml` 文件中 `[project.optional-dependencies]` 节点的指定分组下, 例如:

   ```bash
   pdm add pytest --group test
   ```

   会在 `pyproject.toml` 文件中添加如下内容:

   ```toml
   [project.optional-dependencies]
   test = [
       "pytest>=8.3.5",
   ]
   ```

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
requires = ["pdm-backend"]
build-backend = "pdm.backend"
```

默认情况下, PDM 只打包 `src` 目录下的文件, 如果需要打包其他目录下的文件 (或排除某些文件), 可以在 `pyproject.toml` 文件中添加如下配置:

```toml
[tool.pdm.build]
includes = ["other_package/", "clear.py"]
excludes = ["**/__pycache__/"]
source-includes = ["scripts/", "tests/"]
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

打包结果存储在 `dist` 目录中

## 2. 依赖管理

PDM 通过创建 `virtualenv` 虚拟环境来管理依赖, 每个项目都有一个独立的虚拟环境, 通过 PDM 命令对虚拟环境进行管理

另外, PDM 还会创建 `pdm.lock` 文件, 用于对当前项目的依赖进行锁定, 确保项目在不同的机器上运行时, 依赖包的版本一致

### 2.1. 添加依赖

可通过 `pdm add` 命令添加项目依赖包

#### 2.1.1. 从 PyPI 添加依赖

第三方依赖包可通过包名进行安装, PDM 默认从 PyPI 仓库中安装依赖包, 可通过 `--index-url/-i` 参数指定 PyPI 镜像地址

```bash
pdm add <package_name>
```

或

```bash
pdm add <package_name> -i https://pypi.tuna.tsinghua.edu.cn/simple
```

也可以对现有依赖进行版本更新

```bash
pdm add <package_name> -U
```

如果指定的依赖包在 PyPI 仓库中不存在, 则会返回安装失败的错误

依赖安装后会更新 `pyproject.toml` 文件的 `[project]` 节点下的 `dependencies` 数组项

可通过 `pdm config` 命令来指定 PyPI 镜像地址

```bash
pdm config pypi.url https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 2.1.2. 从本地添加依赖

可以通过 `pdm add` 命令添加本地依赖包

```bash
pdm add <package_path>
```

例如

```bash
pdm add ../pdm_lib
```

此时会在 `pyproject.toml` 文件的 `[project]` 节点下的 `dependencies` 数组项中添加本地依赖包

```toml
[project]
...
dependencies = [
    "pdm-lib @ file:///${PROJECT_ROOT}/../lib",
]
```

#### 2.1.3. 删除依赖

通过如下命令可删除已安装的依赖包

```bash
pdm remove <package_name>
```

依赖删除后会更新 `pyproject.toml` 文件的 `[project]` 节点下的 `dependencies` 数组项

### 2.2. 添加依赖到分组

如要将依赖安装到 `pyproject.toml` 文件中 `[dependency-groups]` 配置项的 `dev` 分组下, 可执行如下命令:

```bash
pdm add pytest pycln mypy autopep8 -d
# 或
pdm add pytest pycln mypy autopep8 --dev
```

如要将依赖安装到 `pyproject.toml` 文件中 `[project.optional-dependencies]` 配置项的指定分组下, 可执行如下命令:

```bash
pdm add pytest --group test
# 或
pdm add pycln mypy autopep8 -G lint
```

要删除指定分组内的依赖包, 需要通过 `remove` 命令:

```bash
pdm remove pytest pycln mypy autopep8 --dev
pdm remove pytest --group test
pdm remove lint pycln mypy autopep8 --group lint
```

### 2.3. 同步依赖

执行如下命令可以根据 `pyproject.toml` 文件中的依赖项, 重新生成 `.venv` 目录中安装的依赖项目, 更新 Python 虚拟环境

```bash
pdm sync [-d/--dev]
# 或
pdm sync [--prod/--production]
# 或
pdm sync [-G/--group <group>]
# 或
pdm sync [-G/--group:all]
# 或
pdm sync [--without <group>]
# 或
pdm sync [--no-default]
```

### 2.4. 同步 `pdm.lock` 文件

执行如下命令可以根据 `pyproject.toml` 文件中的依赖项, 重新生成 `pdm.lock` 文件

```bash
pdm lock [-d/--dev]
# 或
pdm lock [--prod/--production]
# 或
pdm lock [-G/--group <group>]
# 或
pdm lock [-G/--group:all]
# 或
pdm lock [--without <group>]
# 或
pdm lock [--no-default]
```

## 3. 执行 Python 脚本

PDM 可以直接执行当前项目中的任意 `.py` 文件或当前项目虚拟环境下安装的任意 Python 工具包 (例如 `pytest`)

### 3.1. 运行指定的 `.py` 文件

可以通过 PDM 的 `run` 命令来运行项目中指定的 `.py` 文件, 例如:

```bash
pdm run main.py
```

### 3.2. 运行指定 Python 工具包

如果在当前项目的虚拟环境下安装了 Python 工具包, 那么可以通过 PDM 的 `run` 命令来运行它, 例如:

```bash
pdm run pytest

pdm run pycln .
pdm run mypy .
pdm run autopep8 .
```

各工具执行时, 会读取各自的配置文件, 或从 `pyproject.toml` 中读取该工具的配置, 参见 [配置工具链](#123-配置工具链)

### 3.3. 指定运行脚本

可以通过 `pyproject.toml` 中的 `[tool.pdm.scripts]` 配置项来设置运行脚本, 并通过 `pdm run <script_name>` 来运行指定的脚本, 例如:

```toml
[tool.pdm.scripts]
start = "main.py"
check = { composite = ["pycln .", "mypy .", "autopep8 ."] }
test = "pytest tests"
clean = { call = "clear:main" }
```

上述脚本可通过如下命令运行:

```bash
pdm run start
pdm run check
pdm run test
pdm run clean
```

## 4. 打包构建

通过以下命令可以将当前项目打包为 `.whl` 文件, 并指定启动脚本用于启动项目

相关打包构建器的配置可参见 [配置打包构建器](#124-配置打包构建器)

另外需要定义项目的启动脚本, 需要在 `pyproject.toml` 文件中添加如下配置:

```toml
[project.scripts]
pdm-package = "pdm_package:run"
```

执行如下命令可以将当前项目进行打包构建

```bash
pdm build
```

命令执行完毕后, 会在 `dist` 目录中生成 `pdm_package-0.1.0-py3-none-any.whl` 文件

该文件可通过 `pip install` 命令安装到其它项目环境中

```bash
pip install pdm_package-0.1.0-py3-none-any.whl
```

安装完毕后, 即可通过启动脚本启动项目

```bash
pdm-package
```
