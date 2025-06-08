# PDM for Application

通过 PDM 可以创建 Python 应用项目, 这类项目一般会直接执行, 不会打包为 `.tar.gz` 或 `.whl` 包文件, 故项目结构较 `package` 或 `lib` 类型简单

## 1. 创建项目

在 `pdm new` 或 `pdm init` 命令的交互式问题中, 将如下问题回答为 `n`, 即可创建 Flat 代码布局的 Python 项目

```plaintext
Do you want to build this project for distribution(such as wheel)?
If yes, it will be installed by default when running `pdm install`. [y/n] (n): n
```

这样会创建一个 Flat Layout 结构的项目, 所有的模块都位于项目根目录下

```plaintext
.
├── tests
│   └── __init__.py
├── README.md
├── main.py
├── pyproject.toml
└── pdm.lock
```

### 2. 配置项目

一般情况下, Application 类型项目无需打包, 可在 `pyproject.toml` 文件中添加如下配置

```toml
[tool.pdm]
distribution = false
```

此配置禁止将当前项目作为一个可编辑依赖进行安装, 参考 [安装项目依赖](../README.md#34-安装项目依赖)
