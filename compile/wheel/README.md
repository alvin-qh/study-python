# 使用 Wheelhouse

通过 Wheel 工具可以制作本地安装包, 即根据 `requirements.txt` 文件将依赖的 Python 包下载保存为 `*.whl` 文件, 并在目标环境中通过这些 `*.whl` 文件离线安装依赖包

## 1. 创建虚拟环境

### 1.1. 创建虚拟环境

```bash
python -m venv .venv --prompt=compile-wheel
```

### 1.2. 进入虚拟环境

```bash
source .venv/bin/activate
```

### 1.3. 安装依赖

安装开发环境依赖

```bash
pip install -r requirements.txt
```

安装生产环境依赖

```bash
pip install -r requirements-prod.txt
```

## 2. 使用 Wheelhouse

### 2.1. 导出依赖

在当前项目的 Python 虚拟环境中执行

```bash
pip wheel -r requirements.txt -w .wheelhouse
```

上述命令可以将 [requirements.txt](./requirements.txt) 文件中定义的依赖下载到 `wheelhouse` 文件夹内

### 2.2. 安装依赖

在当前项目的 Python 虚拟环境中执行

```bash
pip install --no-index --find-links=./.wheelhouse -r requirements.txt
```

上述命令可以根据 `requirements.txt` 文件中定义的依赖, 从 `.wheelhouse` 文件夹内获取依赖文件 (`.whl` 文件) 并安装依赖包
