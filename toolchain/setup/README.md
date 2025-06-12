# Setuptools

Setuptools 是 Python 官方提供的基本打包工具, 可以将当前 Python 项目安装到指定 Python 环境, 或将其打包进行分发

## 1. 安装配置

### 1.1. 安装 Setuptools

Setuptools 相当于是一个 Python 依赖包, 通过 pip 进行安装即可

```bash
pip install -U setuptools
```

Setuptools 的配置文件为 `setup.py`, 即一段 Python 脚本

### 1.2. 配置 `setup.py` 脚本

一个典型的 `setup.py` 脚本如下:

```python
from setuptools import setup, find_packages

from os import path

# 获取当前目录
CURRENT_DIR = path.abspath(path.dirname(__file__))


def load_readme() -> str:
    """加载当前目录下的 `README.md` 文件

    Returns:
        str: `README.md` 文件内容
    """
    with open(path.join(CURRENT_DIR, "README.md"), "r", encoding="utf-8") as f:
        return f.read()


# 执行 `setup` 函数, 打包当前项目
setup(
    name="toolchain-setup",
    version="0.0.1",
    classifiers=[
        "Development Status :: 3 - Production",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="Setup toolchain demo",
    author="Alvin",
    author_email="quhao317@163.com",
    license="MIT",
    long_description=load_readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(include=["toolchain_setup"]),
    package_dir={"": "."},
    include_package_data=True,
    package_data={
        "toolchain_setup": [
            "conf/*.json",
        ],
    },
    install_requires=[
        "click>=8.1.8",
    ],
    extras_require={
        "test": [
            "pytest>=8.3.5",
            "pytest-sugar>=1.0.0",
        ],
        "type": [
            "mypy>=1.15.0",
            "mypy_extensions>=1.1.0",
        ],
        "lint": [
            "autopep8>=2.3.2",
            "pycln>=2.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "toolchain-setup=toolchain_setup.main:main",
        ],
    },
)
```

`setup` 函数的参数列表指定了项目打包的各项配置信息, 其中大部分参数都是可选的, 用于生成的程序包上传到 PyPI 网站时所需的各类信息

其中的关键参数包括:

1. `name`: 项目名称, 也即打包后的包名称;
2. `version`: 项目版本号;
3. `classifiers`: 项目的分类信息, 用于 PyPI 网站的索引, 详情请查看 [PyPI 分类信息](https://pypi.org/classifiers/);
4. `description`: 项目的描述信息;
5. `author`: 项目作者;
6. `author_email`: 项目作者的邮箱;
7. `license`: 项目的许可证;
8. `long_description`: 项目的详细描述信息, 一般使用 Markdown 格式;
9. `long_description_content_type`: 详细描述信息的内容类型, 一般为 `text/markdown`;
10. `packages`: 项目的 Python 包列表, 即需要打包的 Python 包名;
11. `package_data`: 打包除 Python 包以外的其他文件, 如静态文件, 配置文件等;
12. `install_requires`: 要安装的支持本项目执行的依赖包列表;
13. `extras_require`: 要安装的支持本项目的其它依赖包列表;
14. `entry_points`: 项目的入口点, 即在命令行中可以执行的命令;
15. `scripts`: 其它的可执行脚本文件路径, 在当前包安装后, 这些脚本会被复制到系统的 `/usr/bin` 目录下;

## 2. 安装和打包

### 2.1. 安装当前项目

执行如下命令可以将当前项目安装到当前的 Python 环境中:

```bash
python setup.py install
```

之后即可通过 `toolchain-setup` 命令执行当前项目, 执行脚本由 `setup.py` 文件中 `setup` 函数的 `entry_points` 参数项指定;

### 2.2. 打包当前项目

#### 2.2.1. 打包为 `tar.gz` 文件

执行如下命令可以将当前项目打包成 `tar.gz` 文件:

```bash
python setup.py sdist
```

打包输出到 `dist` 目录下, 本例打包为 `dist/toolchain-setup-0.0.1.tar.gz` 文件;

要安装打包为 `tar.gz` 文件的当前项目, 可以执行如下命令:

```bash
# 将项目打包解压缩
tar -xvf toolchain_setup-0.0.1.tar.gz

# 进入解压后的目录
cd toolchain_setup-0.0.1

# 安装项目
python setup.py install
```

#### 2.2.2. 创建 `wheel` 包

创建 `wheel` 包, 可以执行如下命令:

```bash
python setup.py bdist_wheel
```

创建 `wheel` 包后, 会在 `dist` 目录下生成 `.whl` 文件, 本例会生成 `dist/toolchain_setup-0.0.1-py3-none-any.whl` 文件

可以通过如下命令安装 `wheel` 包:

```bash
pip install dist/toolchain_setup-0.0.1-py3-none-any.whl
```

也可以同时生成 `tar.gz` 以及 `wheel` 包:

```bash
python setup.py sdist bdist_wheel
```

### 2.3. 使用 `build` 工具

通过 `python setup.py ...` 命令执行打包的方式已经废弃, 后续不再继续支持, Python 推荐使用更新的 `build` 命令进行打包

#### 2.3.1. 安装 `setup` 工具

在当前 Python 环境, 执行安装:

```bash
pip install -U build
```

#### 2.3.2. 执行打包

确保当前目录下存在 `setup.py` 文件, 并执行如下命令:

```bash
python -m build
```

执行结束后

## 3. `setup.cfg` 文件

除了通过 `setup.py` 脚本进行打包外, 还可以使用 `setup.cfg` 文件进行打包, `setup.cfg` 文件的格式为 `ini` 格式

```ini
[metadata]
name = toolchain-setup
version = 0.0.1
classifiers =
    Development Status :: 3 - Production
    Programming Language :: Python
    Intended Audience :: Developers
    Operating System :: OS Independent
    Programming Language :: Python :: 3.8
    Programming Language :: Python :: 3.9
description = Setup toolchain demo
author = Alvin
author_email = quhao317@163.com
license = MIT
long_description = file: README.md
long_description_content_type = text/markdown

[options]
package_dir =
    =.
packages = find:
include_package_data = True
install_requires =
    click>=8.1.8

[options.packages.find]
where = .
include =
    toolchain_setup

[options.package_data]
toolchain_setup =
    conf/*.json

[options.entry_points]
console_scripts =
    toolchain-setup=toolchain_setup.main:main

[options.extras_require]
test =
    pytest>=8.3.5
    pytest-sugar>=1.0.0
type =
    mypy>=1.15.0
    mypy_extensions>=1.1.0
lint =
    autopep8>=2.3.2
    pycln>=2.5.0
```

可以看到, `setup.cfg` 配置文件中包括的定义可以和 `setup.py` 文件中 `setup` 函数的参数定义一一对应, 但 `setup.cfg` 文件采用 `ini` 格式, 其中的配置项具备层次, 而非 `setup.py` 脚本中 `setup` 函数的参数列表为平面结构, 因此 `setup.cfg` 配置文件更容易阅读和管理

项目中一旦包含了 `setup.cfg` 文件, 那么 `setup.py` 文件就只需要包含一行代码即可:

```python
from setuptools import setup

setup()
```

当然, `setup.py` 文件的 `setup` 函数也可以继续包含参数, 但如果参数与 `setup.cfg` 中的配置冲突, 则以 `setup.cfg` 中的配置为准

可以继续沿用如下的打包方法:

```bash
python setup.py install
python setup.py sdist bdist_wheel

# 或
python -m build
```

## 4. `pyproject.toml` 文件

在现代化 Python 项目中, `setup.py` 文件已经不再被推荐使用, Python 推荐使用 `pyproject.toml` 文件进行打包, `pyproject.toml` 文件的格式为 `toml` 格式, 具有更丰富的表达能力

### 4.1. 文件内容

一个典型的 `pyproject.toml` 文件内容如下:

```toml
[project]
name = "toolchain-setup"
version = "0.1.0"
description = "Setup toolchain demo"
readme = "README.md"
requires-python = ">=3.13"
authors = [
    { name = "Alvin", email = "quhao317@163.com" },
]
classifiers = [
    "Development Status :: 3 - Production",
    "Programming Language :: Python",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]
license = "MIT"
dependencies = [
    "click>=8.1.8",
]

[dependency-groups]
lint = [
    "autopep8>=2.3.2",
    "pycln>=2.5.0",
]
type = [
    "mypy>=1.15.0",
    "mypy_extensions>=1.1.0",
]
test = [
    "pytest>=8.3.5",
    "pytest-sugar>=1.0.0",
]

[project.scripts]
toolchain-setup = "toolchain_setup.main:main"

[build-system]
requires = [
    "setuptools>=80.7.1",
    "setuptools-scm>=8.3.1",
]
build-backend = "setuptools.build_meta"

[tool.setuptools]
package-dir = { '' = '.' }
include-package-data = true

[tool.setuptools.packages.find]
exclude = ['tests']

[tool.setuptools.package-data]
"toolchain_setup" = [
    "conf/*.json",
]

[tool.pycln]
path = "."
all = true
exclude = '\.history|build'

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
exclude = '\.history|build'

[tool.autopep8]
max_line_length = 120
ignore = ['E501', 'W6']
in-place = true
recursive = true
jobs = -1
aggressive = 3
exclude = '.history/**,build/**'

[tool.pytest.ini_options]
addopts = [
    '-s',
]
testpaths = [
    'tests',
]
```

`pyproject.toml` 文件有如下特点:

- 采用 `.toml` 格式, 具备更丰富的表达能力
- 包含了 `setup.cfg` 文件中的全部内容
- 包含 `[tool.xxx]` 配置段, 可作为多种 Python 工具 (如 `pytest`, `mypy`, `autopep8`, `pycln` 等) 的配置文件

### 4.2. 安装依赖

可以通过 PIP 工具, 通过 `pyproject.toml` 文件为当前 Python 环境安装依赖, 相比通过 `requirements.txt` 文件安装依赖, `pyproject.toml` 文件的依赖包含更为清晰

```bash
pip install . --group lint --group type --group test
```

可以通过 `--group` 参数指定从 `[dependency-groups]` 配置下包含的依赖组

### 4.3. 执行打包

具备`pyproject.toml` 文件的项目, 无需再包含 `setup.py` 文件, 即可通过如下命令构建项目:

```bash
python -m build
```

该命令会同时构建 `sdist` (`.tar.gz`) 和 `wheel` (`.whl`) 包, 并将构建结果保存在 `dist` 目录下
