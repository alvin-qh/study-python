# PDM

`lib` 目录中为一个 Python 库, `app` 中为调用该库的应用程序

## 1. 项目类型

PDM 可以将程序初始化为**库**类型或**应用**类型项目, 这二者有一些不同点

在调用 `pdm init` 进行初始化库类型项目时, 可以在第 2 步指定项目类型

```bash
Please select (0): 2
Is the project a library that is installable?
If yes, we will need to ask a few more questions to include the project name and build backend [y/n] (n):
```

库类型项目和应用类型项目的区别都体现在 `pyproject.toml` 文件中, 具体如下:

1. `[project]` 配置

   库类型项目必须包含 `name` 和 `version` 属性, 而应用类型项目则不需要;

1. `[build-system]` 配置

   库类型项目必须包含 `[build-system]` 配置, 表示项目构建工具, 可选的构建工具包括: `pdm-backend`, `setuptools`, `flit-core` 以及 `hatchling`, 推荐使用 `pdm-backend`, 配置如下:

   ```ini
   [build-system]
   requires = ["pdm-backend"]
   build-backend = "pdm.backend"
   ```

1. `[tool.pytest.ini_options]` 配置

   库类型项目的 `pythonpath` 可以为 `"."`, 因为库类型项目会将项目本身作为一个 "editable library" 进行安装; 而应用类型的 `pythonpath` 必须为 `"src"`, 否则找不到 `src` 目录下的模块

## 2. 安装依赖

PDM 可以管理三种不同来源的依赖库

1. PyPI 依赖库, 即 Python 官方依赖库, 直接通过 `pdm add [--dev] [-G <name>]` 进行安装, 例如

   ```bash
   pdm add flask
   pdm add pytest --dev
   pdm add autopep8 -G lint
   ```

2. GIT 依赖库, 可以直接添加

   ```bash
   pdm add git+ssh://github.com/path/lib.git#1.0.0
   ```

   或

   ```bash
   pdm add git+https://github.com/path/lib.git#1.0.0
   ```

   为避免在使用 http/https 链接时, 每次输入密码, 可以通过 git 的 store 功能记住密码

   ```bash
   git config --global credential.helper store
   ```

   或者在 `~/.git/config` 中添加

   ```ini
   [credential]
   helper = store
   ```

3. 当前文件系统依赖, 即所依赖的库位于当前磁盘中, 即

   ```bash
   pdm add ../lib
   ```

   此时会给 `pyproject.toml` 文件中添加如下内容

   ```ini
   [project]
   dependencies = [
      "some-python-lib @ file:///${PROJECT_ROOT}/../lib",
   ]
   ```
