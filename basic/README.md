# Python Basic

- [Python Basic](#python-basic)
  - [1. 使用 PyEnv](#1-使用-pyenv)
    - [1.1. 安装](#11-安装)
    - [1.2. 配置](#12-配置)
    - [1.3. 管理 Python 版本](#13-管理-python-版本)
  - [2. 使用 VirtualEnv](#2-使用-virtualenv)
    - [2.1. 创建虚拟环境](#21-创建虚拟环境)
    - [2.2. 使用虚拟环境](#22-使用虚拟环境)
  - [3. 使用 PDM](#3-使用-pdm)
    - [3.1. 安装](#31-安装)
    - [3.2. 初始化项目](#32-初始化项目)
    - [3.3. 管理依赖](#33-管理依赖)
    - [3.4. 执行 Python 命令](#34-执行-python-命令)
    - [3.5. 设置 pdm](#35-设置-pdm)
    - [3.6. 构建打包](#36-构建打包)

## 1. 使用 PyEnv

参见官网 <https://github.com/pyenv/pyenv>

### 1.1. 安装

通过自动安装脚本

```bash
curl https://pyenv.run | bash
```

或者从 <https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer> 下载安装脚本, 通过 `bash` 执行

### 1.2. 配置

在启动脚本中加入如下命令

```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
```

### 1.3. 管理 Python 版本

列出所有可按照版本

```bash
pyenv install --list
```

安装指定版本

```bash
pyenv install <指定版本号>
```

在安装 Python 时, 可能会产生编译依赖错误, 需要安装如下依赖

```bash
# On Debian/Ubuntu/Linux Mint
sudo apt install curl git-core gcc make zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev libssl-dev

# On CentOS/RHEL
sudo yum -y install epel-release
sudo yum -y install git gcc zlib-devel bzip2-devel readline-devel sqlite-devel openssl-devel

# On Fedora 22
sudo yum -y install git gcc zlib-devel bzip2-devel readline-devel sqlite-devel openssl-devel
```

切换版本

```bash
# 切换全局 Python 版本
pyenv global <指定版本号>

# 切换当前目录 Python 版本
pyenv local <指定版本号>
```

## 2. 使用 VirtualEnv

VirtualEnv 是 Python 传统的包管理方案

> 本项目已经通过 `pyproject.toml` 文件进行项目管理, 并使用 src layout 目录结构, 所以无法直接使用 virtualenv 的方式

### 2.1. 创建虚拟环境

在当前项目的 `.venv` 目录下创建虚拟环境, 名称为 `basic`

```bash
python -m venv .venv --prompt='basic'
```

### 2.2. 使用虚拟环境

```bash
# 进入虚拟环境
source .venv/bin/activate

# 退出虚拟环境
deactivate
```

## 3. 使用 PDM

pdm 是符合 Python 最新标准 (PEP 517 + PEP 621) 的包管理器

### 3.1. 安装

使用 Linux 自带的 Python 3 安装 pdm

```bash
/usr/bin/pip3 install --user pdm
```

如果系统为安装 pip 工具, 按如下命令安装

```bash
sudo apt install pip
```

安装完毕后, 会在当前用户的 `~/.local/bin/` 目录下建立可执行文件, 需要将该目录加入到 `PATH` 环境变量中

### 3.2. 初始化项目

执行如下命令初始化 Python 项目

```bash
pdm init
```

此时会在当前目录下建立 `.venv` 目录和 [pyproject.toml](./pyproject.toml) 文件, 其中:

- `.venv` 目录下为当前项目的 virtualenv 虚拟环境
- [pyproject.toml](./pyproject.toml) 为项目配置文件

另外会建立 `src` 目录和 `tests` 目录, 分别用来存放项目源代码和测试代码

### 3.3. 管理依赖

通过 pdm 可以直接添加或删除依赖

```bash
# 添加依赖
pdm add <依赖包名称>

# 删除依赖
pdm remove <依赖包名称>
```

例如: `pdm add pytest` 或 `pdm remove pytest`

### 3.4. 执行 Python 命令

通过 pdm 可以直接执行当前虚拟环境下的 Python 命令

```bash
pdm run <Python 命令>
```

例如: `pdm run pytest`

### 3.5. 设置 pdm

通过 `pdm config` 命令可以设置 pdm 的一些配置, 例如设置包下载网站的镜像

```bash
pdm config pypi.url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3.6. 构建打包

如果当前项目是一个 Python 库, 则可以对其进行构建打包

```bash
pdm build
```
