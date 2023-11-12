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

### 2.2. 执行代码检查

```bash
pdm check
```

### 2.3. 执行测试

```bash
pdm test
```
