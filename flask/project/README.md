# Study Python - Flask

## 1. Setup

### 1.1 Install pyenv

- On macOS

```bash
$ brew install pyenv
$ brew install pyenv-virtualenv
```

- On Linux

````bash
$ curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
````

### 1.2 Setup pyenv

Edit `~/.bash_profile`, `~/.bashrc` or `~/.zshrc` file, add the following content:

```bash
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

### 1.3 Install python

- Check if `python 3.8.5` installed;

  ```bash
  $ pyenv versions
  ```

- Install `python 3.8.5`

  ```bash
  $ pyenv install 3.8.5
  ```

  > 注意：如果因下载过慢而无法安装成功，可通过提示的下载路径，通过其它下载工具下载安装压缩包，放入`~/.pyenv/cache`目录下，例如：`~/.pyenv/cache/Python-3.8.5.tar.xz`

- 使用`python 3.8.5`

  ```bash
  $ pyenv local 3.8.5
  ```

### 1.4 Create and active virtualenv

```bash
$ python -m venv .venv --prompt='study-python-basic-notebook'
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

### 1.5 Enable "Jupyterlab Code Formatter" extension

```bash
$ jupyter labextension install @ryantam626/jupyterlab_code_formatter
$ jupyter serverextension enable --py jupyterlab_code_formatter
```

Tips:  
如果上述命令安装非常慢，可能是由于 node.js 的 yarn 镜像设置的不对，可以为 yarn 设置国内镜像以加快安装速度
```
$ yarn config set registry https://registry.npm.taobao.org --global
$ yarn config set disturl https://npm.taobao.org/dist --global
```

> [Jupyterlab Code Formatter Homepage](https://jupyterlab-code-formatter.readthedocs.io/)

### 1.6 Start "jupyterlab" and setup

- Start "jupyterlab server"

  ```bash
  $ jupyter lab --no-browser
  ```

  After command run successful, then the url with token should be printed, open the url with browser

- Click menu `Settings`>`Advanced Settings Editor`>`Jupyterlab Code Formatter`，add content：

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

- Click menu `Settings`>`Advanced Settings Editor`>`Keyboard Shortcuts`，add content：

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
