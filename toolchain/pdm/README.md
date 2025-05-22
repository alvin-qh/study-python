# PDM Toolchain

参考: <https://pdm-project.org/zh-cn/latest>

## 1. 安装 PDM

### 1.1. Linux/Mac

安装

```bash
curl -sSL https://pdm-project.org/install-pdm.py | python3 -
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

```bash
pdm add <dependency-name>  # 如 pdm add numpy
pdm add <dependency-name==version>  # 如 pdm add numpy==2.2
pdm add <dependency-name>=version>  # 如 pdm add numpy>=2.2
pdm add <dependency-name[optional]>  # 如 pdm add requests[socks]

pdm add <path-to-package>  # 如 pdm add ./libs/data-requirement
pdm add <url-to-package>  # 如 pdm add https://github.com/explosion/spacy-models/releases/download/en_core_web_trf-3.5.0/en_core_web_trf-3.5.0-py3-none-any.whl

pdm add "git+<git-repo-url>" # 如 pdm add "git+https://github.com/pypa/pip.git@22.0"
pdm add "name @ git+<git-repo-url>" # 如 pdm add "pip @ git+https://github.com/pypa/pip.git@22.0"
                                    # 或 pdm add "git+https://github.com/pypa/pip.git@22.0#egg=pip"
pdm add "git+<git-repo-url#egg=<name>&subdirectory=<subpath>>" # 如 pdm add "git+https://github.com/owner/repo.git@master#egg=pkg&subdirectory=subpackage"
```

> 要对 git 使用 ssh 方案，只需将 `https://` 替换为 `ssh://git@`

### 3.2. 添加开发依赖

在 `[dependency-groups]` 中添加分组依赖, 用于当前项目开发环境依赖, 这部分依赖不会被引入到发布的软件包元数据中

```bash
pdm add <dependency> --dev/-d # 添加到 `dev` 分组中
pdm add <dependency> -dG <group-name> # 添加到指定名称的分组中
```

### 3.3. 添加可选依赖

在 `[project.optional-dependencies]` 中添加分组依赖, 这部分依赖作为当前项目的可选依赖, 可以选择性安装

```bash
pdm add <dependency> --group/-G <group-name> # 添加到指定名称的分组中
```

## 4. 项目安装

项目安装会完成两件工作

- 安装当前项目中全部的所需依赖;
- 如果当前项目是 `lib` 或 `package` 类型的, 则将 `src` 目录下的内容作为当前项目的可编辑依赖进行安装
