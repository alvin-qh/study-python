# Tox

Tox 是一个 Python 上的测试管理框架, 可以按分类执行多组测试, 包括不同 Python 版本或不同依赖包版本, 也可以包括单元测试, 集成测试, 代码样式检查, 类型检查等

## 1. 安装

Tox 就是一个 Python 包, 所以可以通过各种方式安装, 包括通过 pip, uv, pdm, poetry 等

Pip

```bash
pip install tox
```

UV

```bash
uv add tox --dev
# 或
uv tool install tox
```

PDM

```bash
pdm add tox --dev
```

Poetry

```bash
poetry add tox --dev
```

## 2. 配置

当前路径下的如下文件均可以作为 tox 配置文件:

- `tox.ini`
- `setup.cfg` (也为 `ini` 格式)
- `pyproject.toml`
- `tox.toml`

更多配置相关内容参考 <https://tox.wiki/en/latest/config.html>

### 2.1 tox.toml
