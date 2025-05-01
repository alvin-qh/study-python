# Package Layout

## 1. 简介

UV 支持通过 Package 模式来组织代码, 以方便代码管理

通过 Package 模式, 代码的布局如下所示:

```plaintext
.
├── src
│   ├── app
│   │   ├── __init__.py
│   │   └── main.py
│   └── lib
│       └── __init__.py
├── test
│   └── lib
│       └── test_func.py
├── pyproject.toml
├── README.md
└── uv.lock
```

可以看到, Package 模式下可包含 `src` 目录和 `test` 目录, 分别用于存放源代码和测试代码

Package 模式代码的发布是通过打包来完成的, 最终
