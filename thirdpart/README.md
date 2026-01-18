# Third Party Libraries Study

本项目包含多个Python第三方库的学习示例, 每个子目录对应一个独立的库进行学习和实践

## 项目列表

### 1. blinker

- **库**: `blinker>=1.9.0`
- **描述**: 信号/事件系统库, 实现了发布-订阅模式支持命名信号和匿名信号, 用于组件间的松耦合通信
- **主要功能**: 创建命名信号, 订阅信号, 发送信号, 装饰器方式连接处理函数
- **文档**: [官方文档](https://pythonhosted.org/blinker/)

### 2. click

- **库**: `click>=8.3.1`
- **描述**: 命令行界面创建库, 用于构建优美的命令行应用程序
- **主要功能**: 定义命令行参数和选项, 创建子命令, 处理用户输入, 验证输入
- **文档**: [官方文档](https://click.palletsprojects.com/)

### 3. dotenv

- **库**: `python-dotenv>=1.2.1`
- **描述**: 环境变量管理库, 从 `.env` 文件加载环境变量到应用中
- **主要功能**: 加载 `.env` 文件, 解析环境变量, 支持不同格式的环境变量定义
- **文档**: [官方文档](https://pypi.org/project/python-dotenv/)

### 4. invoke

- **库**: `invoke>=2.2.1`, `colorama>=0.4.6`
- **描述**: 任务自动化库, 类似于Fabric的任务运行器, 用于定义和执行CLI任务
- **主要功能**: 定义可重用的任务, 自动命令行解析, 任务依赖管理, 彩色输出支持
- **文档**: [官方文档](https://www.pyinvoke.org/)

### 5. loguru

- **库**: `loguru>=0.7.3`
- **描述**: 增强型Python日志库, 提供更美观, 功能更丰富的日志记录体验
- **主要功能**: 简单API配置日志, 日志格式化, 日志文件轮转, 彩色日志输出, 异常完整跟踪
- **文档**: [官方文档](<https://loguru.readthedocs.io/>)

### 6. pretty_errors

- **库**: `pretty-errors>=1.2.25` (dev依赖)
- **描述**: 错误输出美化库, 使Python异常信息更清晰易读
- **主要功能**: 美化异常输出, 自定义配置, 彩色显示, 代码片段高亮, 本地变量显示
- **文档**: [GitHub仓库](https://github.com/onelivesleft/PrettyErrors/)

### 7. zstandard

- **库**: `zstandard>=0.25.0`
- **描述**: Zstandard压缩算法的Python绑定, 提供高性能的数据压缩功能
- **主要功能**: 数据压缩/解压缩, 流式压缩, 字典支持, 并行处理
- **文档**: [官方文档](https://python-zstandard.readthedocs.io/)

## 使用说明

每个子目录都是独立的Python项目, 使用PDM作为包管理器

### 运行项目

```bash
# 进入项目目录
cd <project_name>

# 安装依赖
pdm install

# 运行项目
pdm run start

# 运行测试
pdm run test

# 代码检查
pdm run check
```

## 技术栈

- **Python**: >= 3.13
- **包管理器**: PDM
- **代码质量**: mypy (类型检查), autopep8 (代码格式化), pycln (代码清理)
- **测试框架**: pytest

## License

MIT
