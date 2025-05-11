# Conda

Conda 是一个集成化的 Python 包管理工具, 其基本用法和功能均和 PIP 工具类似, 所以 Conda 不被认为是现代化 Python 包管理工具

Conda 的主要用途在于科学计算, 其自身附带了许多科学计算库, 包括 NumPy, SciPy, Matplotlib, Pandas, Scikit-learn, Scikit-image 等, 故 Conda 的安装文件非常大

Miniconda 是 Conda 的一个轻量级版本, 只包含 Conda 核心功能, 不包含任何科学计算库

## 1. 安装 Miniconda

### 1.1. 下载 Miniconda 安装包

将 Miniconda 的安装包下载到当前目录下

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ./miniconda.sh
```

### 1.2. 安装 Miniconda

执行安装命令

```bash
bash miniconda.sh -b -u -p ~/miniconda3
```

## 2. 配置 Miniconda

Conda 和 PIP 类似, 也是通过 Virtualenv 方式来管理 Python 环境, 但 Conda 默认会在 `~/miniconda3/envs` 目录下对虚拟环境进行集中管理, 并在 `.conda/environments.txt` 文件中记录了当前所有的虚拟环境

### 2.1. 进入基础虚拟环境

通过 Conda 的 `activate` 命令即可进入基础虚拟环境

```bash
bash ~/miniconda3/bin/activate
```

此时即可使用 `conda` 命令进行操作, 例如:

```bash
conda info
```

可查看当前 Conda 环境的信息

### 2.2. 配置 Shell 环境 (可选)

为了方便使用, 可以在配置令 Shell 启动时自动进入 Conda 的基础虚拟环境

配置 ZSH 环境

```bash
conda init zsh
```

配置 Bash 环境

```bash
conda init bash
```

配置所有 Shell 环境

```bash
conda init --all
```

配置后, 一旦系统进入 Shell 环境, 就会自动进入 Conda 的基础虚拟环境, 但这样会与其它 Python 包管理器创建的虚拟环境冲突

如果需要同时使用多种 Python 包管理器, 则可忽略当前步骤, 进入 Shell 后, 通过 [进入基础虚拟环境](#21-进入基础虚拟环境) 介绍的方法手动进入基础虚拟环境

### 2.3. 配置包下载镜像源

为了加快国内下载 Python 包的速度, 可以为 Conda 配置国内的包镜像源, 可通过 `conda config` 命令进行设置:

```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/linux-64/
conda config --set show_channel_urls yes
```

配置完毕后, 配置结果会存储在 `.condarc` 文件中, 可以通过 `conda config --show` 命令查看当前配置:

```bash
conda config --show
```

## 3. 使用 Conda

### 3.1. 创建虚拟环境

#### 3.1.1. 创建命名虚拟环境

在进入基础虚拟环境后, 即可为具体的项目创建专用虚拟环境, 执行如下命令

```bash
conda create --name/-n <env_name>
```

将创建一个名为 `<env_name>` 的虚拟环境, 其中 `<env_name>` 为自定义虚拟环境的名称, 该虚拟环境使用当前系统默认的 Python 版本, 如果要指定 Python 版本, 则使用如下命令

```bash
conda create --name/-n <env_name> python=3.13
```

如果还需同时安装额外的 Python 依赖包, 则使用如下命令

```bash
conda create --name/-n <env_name> python=3.13 pip pytest mypy
```

#### 3.1.2. 在指定路径下创建虚拟环境

如果要在特殊路径的路径下创建虚拟环境, 则使用如下命令:

```bash
conda create --prefix/-p <path>
```

例如:

```bash
conda create -p .venv
```

注意, `--name/-n` 和 `--prefix/-p` 不能同时使用, 即要么指定环境名称, 要么指定环境路径

#### 3.1.3. 查看虚拟环境列表

如未作特殊设置, 则创建的虚拟环境的路径默认位于 `~/anaconda3/envs` 目录下, 可以通过 `conda env list` 命令查看已创建的虚拟环境列表

```bash
conda env list
```

#### 3.1.4. 复制虚拟环境

可以将现有的某个虚拟环境复制到其它路径下:

```bash
conda create --clone <env_name> --prefix <other_path>
```

### 3.2. 删除虚拟环境

对于已创建的虚拟环境, 可以使用如下命令删除:

通过虚拟环境名称进行删除:

```bash
conda env remove --name/-n <env_name>
```

通过虚拟环境路径进行删除:

```bash
con env remove --prefix/-p <path>
```

### 3.3. 激活虚拟环境

Conda 虚拟环境必须激活后才能使用, 激活命令和激活 Conda 基础虚拟环境类似

可以先列出所有可用的 Conda 虚拟环境

```bash
conda env list

# conda environments:
#
                       /home/<user>/<path-to-env>/.venv
base                 * /home/<user>/miniconda3
<project-name>         /home/<user>/miniconda3/envs/<project-name>
```

结果中第一列为虚拟环境的名称, 第二列为虚拟环境所在的路径

如果第一列不为空, 则虚拟环境是通过 `--name/-n` 参数创建的, 否则虚拟环境是通过 `--prefix/-p` 参数创建的

对于有名称的虚拟环境, 可以通过如下方式激活:

```bash
conda activate <env-name>
```

而虚拟环境是否具备名称, 都可以通过虚拟环境路径来进行激活:

```bash
conda activate <env-path>
```

### 3.4. 退出虚拟环境

虚拟环境退出, 可以通过如下方式:

```bash
conda deactivate
```

### 3.5. 管理依赖包

要管理依赖包, 需要先激活一个虚拟环境

安装依赖包:

```bash
conda install <package1> <package2> ...
```

例如:

```bash
conda install mypy autopep8 pytest
```

删除依赖包

```bash
conda remove <package1> <package2> ...
```

更新依赖包

```bash
conda update <package1> <package2> ...
```

### 3.5. 导出虚拟环境

可将 Conda 虚拟环境配置导出, 可在创建新虚拟环境是导入该配置:

导出虚拟环境

```bash
conda env export > environment.yml
```

导入虚拟环境

```bash
conda env create -f environment.yml
```

## 4. 本项目 Conda 配置

```bash
# 激活基础环境
bash ~/miniconda3/bin/activate

# 设置依赖镜像地址 (第一次时需要创建)
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/linux-64/
conda config --set show_channel_urls yes

# 创建虚拟环境 (第一次时需要创建)
conda create -n toolchain-conda

# 激活虚拟环境
conda activate toolchain-conda

# 安装依赖包
conda install mypy autopep8 pytest

# 运行测试
bash check.sh
```
