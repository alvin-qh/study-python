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
from setuptools import setup

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
        "License :: OSI Approved :: MIT License",
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
    package_data={
        "toolchain_setup": [
            "conf/*.json",
        ],
    },
    install_requires=[
        "click>=8.1.8",
    ],
    test_requires=[
        "pytest>=8.3.5",
        "pytest-sugar>=1.0.0",
    ],
    extras_requires={
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
    scripts=[
        # "main.py",
    ],
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
13. `test_requires`: 要安装的支持本项目测试的依赖包列表;
14. `extras_require`: 要安装的支持本项目的其它依赖包列表;
15. `entry_points`: 项目的入口点, 即在命令行中可以执行的命令;
16. `scripts`: 其它的可执行脚本文件路径, 在当前包安装后, 这些脚本会被复制到系统的 `/usr/bin` 目录下;

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
