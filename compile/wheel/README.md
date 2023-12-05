# 使用 Wheel

通过 Wheel 工具可以制作本地安装包, 即根据 `requirements.txt` 文件将依赖的 Python 包下载保存为 `*.whl` 文件, 并在目标环境中通过这些 `*.whl` 文件离线安装依赖包

## 1. 下载依赖

```bash
pip wheel -r requirements.txt -w wheelhouse
```

上述命令可以将 `requirements.txt` 文件中定义的依赖下载到 `wheelhouse` 文件夹内, 参考 [download.sh](./download.sh) 文件

## 2. 安装依赖

上述命令可以根据 `requirements.txt` 文件中定义的依赖, 从 `wheelhouse` 文件夹内获取依赖文件, 安装所需的依赖包, 参考 [install.sh](./install.sh) 文件
