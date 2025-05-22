# PDM for Application

通过 PDM 可以创建 Python 应用项目, 这类项目一般会直接执行, 不会打包为 `.tar.gz` 或 `.whl` 包文件, 故项目结构较 `package` 或 `lib` 类型简单

## 1. 创建项目

在 `pdm new` 或 `pdm init` 命令的交互式问题中, 将如下问题回答为 `n`, 即可创建 Flat 代码布局的 Python 项目

```plaintext
Do you want to build this project for distribution(such as wheel)?
If yes, it will be installed by default when running `pdm install`. [y/n] (n): n
```

该类型项目具备 `src` 目录结构, 项目结构如下:

```plaintext
.
├── tests
│   └── __init__.py
├── README.md
├── main.py
├── pyproject.toml
└── pdm.lock
```

Flat 代码布局指的是项目的根目录下面直接包含 Python 包目录以及 Python 模块文件

## 2. 项目配置

项目中的 `pyproject.toml` 文件定义了项目的配置项, 配置内容参见 [PDM 文档](../README.md), 对于 `app` 类型项目, 几项特殊配置项如下:

### 2.1. 允许当前项目安装自身

```toml
[tool.pdm]
distribution = false
```

此配置禁止将当前项目作为一个可编辑依赖， `distribution = false` 为默认值, 故也可以省略上述配置项
