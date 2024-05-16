# Python

## 1. 安装 Python 开发环境

### 1.1. 安装和设置 PyEnv

> 参考: [https://github.com/pyenv/pyenv](https://github.com/pyenv/pyenv)

#### 1.1.1. 在 macOS 上安装

- 通过 brew 安装 PyEnv

    ```bash
    $ brew install pyenv
    $ brew install pyenv-virtualenv
    ```

- 配置 PyEnv

    编辑 `.bash_profile` (或 `.zshrc`) 文件，添加如下内容:

    ```bash
    export PATH="~/.pyenv/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv virtualenv-init -)"
    ```

#### 1.1.2. 在 Linux 上安装

- 下载安装脚本并执行

    > 参考: [https://github.com/pyenv/pyenv-installer](https://github.com/pyenv/pyenv-installer)

    ```bash
    $ curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
    ```

- 配置 PyEnv

    编辑 `.bashrc` (或 `.zshrc`) 文件, 添加如下内容:

    ```bash
    export PATH="~/.pyenv/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv virtualenv-init -)"
    ```

### 1.2. 安装 Python

- 检查已安装的 Python 版本

    ```bash
    $ pyenv versions
        system
      * 3.10.3 (set by /home/<user>/.pyenv/version)
        3.8.5
        3.9.5
    ```

    标记 `*` 的表示默认使用的 Python 版本

- 列出所有可用的 Python 版本

    ```bash
    $ pyenv install --list
    ```

- 安装指定的 Python 版本

    ```bash
    $ pyenv install 3.10.3
    ```

- 设置全局默认的 Python 版本

    ```bash
    $ pyenv global 3.10.3
    ```

## 1.2. 创建虚拟环境

- 在项目路径下，设置本地使用的 Python 版本

    ```bash
    $ pyenv local 3.10.3
    ```

    该命令将创建 `.python-version` 文件，保存指定的 Python 版本号

- 创建虚拟环境（virtualenv）

    ```bash
    $ python -m venv .venv --prompt="project prompt"
    ```

## 2. 安装 JupyterLab

### 2.1. 安装必要的 Python 依赖包

如下 Python 依赖包需要安装:

```plaintext
jupyterlab

jupyterlab_code_formatter
autopep8
jupyter_nbextensions_configurator
lckr-jupyterlab-variableinspector
jupyterlab-lsp
python-language-server[all]
jupyterlab-git>=0.30.0b1
```

- `autopep8`: Python 代码格式化后端
- `jupyterlab_code_formatter`: 代码格式化插件
- `jupyter_nbextensions_configurator`: 扩展管理插件
- `lckr-jupyterlab-variableinspector`: 变量可视化插件
- `jupyterlab-lsp`: 语言服务后端
- `python-language-server[all]`: Python 语言服务后端
- `jupyterlab-git`: Git 管理插件

构建 JupyterLab 环境

```bash
$ jupyter lab build
```

### 2.2. 激活代码格式化插件

```bash
$ jupyter labextension install @ryantam626/jupyterlab_code_formatter
$ jupyter serverextension enable --py jupyterlab_code_formatter
```

提示: 如果上述命令安装非常慢，可能是由于 node.js 的 yarn 镜像设置的不对，可以为 yarn 设置国内镜像以加快安装速度

```bash
$ yarn config set registry https://registry.npm.taobao.org --global
$ yarn config set disturl https://npm.taobao.org/dist --global
```

### 2.3. 启动 JupyterLab 服务

```bash
$ jupyter lab --no-browser
```

从启动打印的日志里，可以获取到浏览器地址，通过浏览器打开即可

### 2.4. 配置代码格式化

1. 点击 Settings / Advanced Settings Editor / Jupyterlab Code Formatter 菜单，添加如下内容

    ```json
    {
        "autopep8": {
        "max_line_length": 120,
        "ignore": [
            "E226",
            "E302",
            "E41"
        ]
        },
        "preferences": {
            "default_formatter": {
                "python": "autopep8",
                "r": "formatR"
            }
        }
    }
    ```

2. 点击 Settings / Advanced Settings Editor / Keyboard Shortcuts 菜单，添加如下内容

    ```json
    {
        "shortcuts": [
            {
                "command": "jupyterlab_code_formatter:autopep8",
                "keys": [
                    "Ctrl K",
                    "Ctrl M"
                ],
                "selector": ".jp-Notebook.jp-mod-editMode"
            }
        ]
    }
    ```
