# Workspace

所谓 Workspace, 可以认为是依赖库的一种统一管理模式, 和独立的库相比, Workspace 模式可以

- 统一管理项目, 即可以在一个目录下管理主项目和其依赖的库项目
- 统一管理虚拟环境, 即主项目和其依赖的库项目使用相同的 Python 虚拟环境, 从而统一管理所有项目的依赖

## 1. 设置 Workspace

本例中, 整个 Workspace 的目录结构如下:

```plaintext
.
├── packages
│   ├── lib
│   │   ├── src
│   │   │   └── uv_workspace_lib
│   │   │       ├── __init__.py
│   │   │       ├── math.py
│   │   │       └── py.typed
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   └── test_uv_workspace_lib.py
│   │   ├── pyproject.toml
│   │   └── README.md
│   └── utils
│       ├── src
│       │   └── uv_workspace_utils
│       │       ├── __init__.py
│       │       ├── mem_io.py
│       │       └── py.typed
│       ├── tests
│       │   ├── __init__.py
│       │   └── test_mem_io.py
│       ├── pyproject.toml
│       └── README.md
├── tests
│   ├── __init__.py
│   └── test_main.py
├── clear.py
├── main.py
├── pyproject.toml
├── README.md
├── tasks.py
└── uv.lock
```

### 1.1. 配置主项目

主项目一般位于根
