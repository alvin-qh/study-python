# PDM for Lib

通过 PDM 可以创建 Python 库项目, 用于编译一个 Python 库, 输出 `.tar.gz` 或 `.whl` 包文件供其它 Python 项目依赖引用

## 1. 创建项目

在 `pdm new` 或 `pdm init` 命令的交互式问题中, 将如下问题回答为 `y`, 即可创建一个可打包 Python 项目

```plaintext
Do you want to build this project for distribution(such as wheel)?
If yes, it will be installed by default when running `pdm install`. [y/n] (n): y
```

该类型项目具备 `src` 目录结构, 项目结构如下:

```plaintext
.
├── src
│   └── <project_name>
│       ├── __init__.py
│       └── py.typed
├── tests
│   └── __init__.py
├── README.md
├── pyproject.toml
└── pdm.lock
```

PDM 会在项目中创建 `src` 目录, 所有的项目源代码都应位于 `src` 目录下, 且 `src` 目录下必须具备一个和项目名相同的包 (本例中为 `pdm_package` 包), 作为当前 Python 库的根包名

对于 `lib` 类型项目, PDM 会将 `src` 目录下的内容作为 "可编辑" 依赖安装到当前的虚拟环境中 (即 `.venv` 目录)

## 2. 项目配置

项目中的 `pyproject.toml` 文件定义了项目的配置项, 配置内容参见 [PDM 文档](../README.md), 对于 `package` 类型项目, 几项特殊配置项如下:

### 2.1. 允许当前项目安装自身

```toml
[tool.pdm]
distribution = true
```

此配置允许当前项目作为一个可编辑依赖, 被安装到当前虚拟环境中

### 2.2. 定义打包器配置

`package` 类型项目需要能够打包安装, 故需要定义打包器配置, 参见 [配置打包构建器](../README.md#71-配置打包构建器) 章节
