# PDM for Package

通过 PDM 可以创建一个可执行并可打包的 Python 项目

## 1. 创建项目

在 `pdm new` 或 `pdm init` 命令的交互式问题中, 将如下问题回答为 `y`, 即可创建一个可打包 Python 项目

```plaintext
Do you want to build this project for distribution(such as wheel)?
If yes, it will be installed by default when running `pdm install`. [y/n] (n): y
```

这样会创建一个 SRC Layout 结构的项目, 该项目结构中包含一个 `src` 目录, 所有的项目源代码都应位于 `src` 目录下, 且 `src` 目录下必须具备一个和项目名相同的包 (本例中为 `pdm_package` 包), 作为当前 Python 库的根包名

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

对于 `package` 类型项目, PDM 会将 `src` 目录下的内容作为 "可编辑" 依赖安装到当前的虚拟环境中 (即 `.venv` 目录), 参考 [安装项目依赖](../README.md#34-安装项目依赖) 章节

## 2. 项目配置

`pyproject.toml` 文件中定义了当前项目的配置项, 参见 [PDM 文档](../README.md), 对于 `lib` 类型项目, 需要添加如下配置:

如下配置允许当前项目作为一个可编辑依赖, 被安装到当前虚拟环境中, 参考 [安装项目依赖](../README.md#34-安装项目依赖) 章节

```toml
[tool.pdm]
distribution = true
```

`package` 类型项目所产生的包, 需要能够在安装后被直接运行, 故需要定义启动脚本, 参见 [配置启动脚本](../README.md#72-配置启动脚本) 章节

`package` 类型项目需要能够打包安装, 需要定义打包器配置, 参见 [配置打包构建器](../README.md#71-配置打包构建器) 章节
