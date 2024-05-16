# Click

## 启动演示程序

方式1: 通过执行 [src/run.py](./src/run.py)

```bash
pdm run run.py click red --name 'Alvin' -l en -c 10
```

方式2: 通过 [pyproject.toml](./pyproject.toml) 中定义的 `[tool.pdm.scripts]/cli` 执行

```bash
pdm run cli click red --name 'Alvin' -l en -c 10
```

方式3: 直接执行

```bash
# 进入虚拟环境
source .venv/bin/activate

# 进入源码目录执行
cd src
python run.py click red --name 'Alvin' -l en -c 10
```
