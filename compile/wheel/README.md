# 使用 Wheelhouse

通过 Wheel 工具可以制作本地安装包, 即根据 `requirements.txt` 文件将依赖的 Python 包下载保存为 `*.whl` 文件, 并在目标环境中通过这些 `*.whl` 文件离线安装依赖包

## 1. 使用 Wheelhouse

### 1.1. 导出依赖

在当前项目的 Python 虚拟环境中执行

```bash
pip wheel -r requirements.txt -w wheelhouse
```

上述命令可以将 [requirements.txt](./requirements.txt) 文件中定义的依赖下载到 `wheelhouse` 文件夹内

### 1.2. 安装依赖

在当前项目的 Python 虚拟环境中执行

```bash
pip install --no-index --find-links=./.wheelhouse -r requirements.txt
```

上述命令可以根据 `requirements.txt` 文件中定义的依赖, 从 `wheelhouse` 文件夹内获取依赖文件 (`.whl` 文件) 并安装依赖包

## 2. 和 PDM 集成

### 2.1. 通过 PDM 安装本地包

下载了 `.whl` 文件后, 即可利用 PDM 安装本地的 `.whl` 文件

```bash
pdm add ./.wheelhouse/flask-3.0.0-py3-none-any.whl
pdm add ./.wheelhouse/pytest-7.4.3-py3-none-any.whl -G test
```

此时, `pyproject.toml` 文件中会包含基于本地文件的依赖

```toml
[project]
...
dependencies = [
    "Flask @ file:///${PROJECT_ROOT}/.wheelhouse/flask-3.0.0-py3-none-any.whl",
    "xxhash @ file:///${PROJECT_ROOT}/.wheelhouse/xxhash-3.4.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    "Werkzeug @ file:///${PROJECT_ROOT}/.wheelhouse/werkzeug-3.0.1-py3-none-any.whl",
]

[project.optional-dependencies]
basic = [
    "pip @ file:///${PROJECT_ROOT}/.wheelhouse/pip-23.3.1-py3-none-any.whl",
    "setuptools @ file:///${PROJECT_ROOT}/.wheelhouse/setuptools-68.2.2-py3-none-any.whl",
]
test = [
    "pytest @ file:///${PROJECT_ROOT}/.wheelhouse/pytest-7.4.3-py3-none-any.whl",
]
lint = [
    "autopep8 @ file:///${PROJECT_ROOT}/.wheelhouse/autopep8-2.0.4-py2.py3-none-any.whl",
    "mypy @ file:///${PROJECT_ROOT}/.wheelhouse/mypy-1.6.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
]
```

### 2.2. 从现有 PDM 项目导出 requirements.txt

对于现有 PDM 项目, 如果要导出 Wheelhouse, 则现需要导出 `requirements.txt` 文件, 通过以下命令即可

```bash
pdm export -f requirements -o requirements.txt --without-hash
```

### 2.3. PDM Script

可以将上述命令集成到 PDM Script 中, 即在 `pyproject.toml` 文件中增加如下内容

```toml
[tool.pdm.scripts]
...
export = "pdm export -f requirements -o requirements.txt --without-hash"
build-wheel = "pip wheel -r requirements.txt -w ./.wheelhouse"
restore-wheel = "pip install --no-index --find-links=./.wheelhouse -r requirements.txt"
```

之后通过 `pdm run` 即可执行这些命令, 例如:

```bash
pdm run export
```
