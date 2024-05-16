# Graphene

参考: <https://graphene-python.org/> 官方网站

## 1. 启动运行环境

```bash
docker compose -f docker/docker-compose.yml up
```

## 2. Python 项目

参考 [pyproject.toml](./pyproject.toml) 文件

### 2.1. 安装依赖

```bash
pdm install -G:all
```

如果在安装 `psycopg2` 时报错, 需要安装编译依赖

```bash
sudo apt install python3-dev libpq-dev
```

之后即可正常执行 `pdm install` 命令

### 2.2. 执行代码检查

```bash
pdm check
```

### 2.3. 执行测试

```bash
pdm test
```
